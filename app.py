from flask import Flask, request, jsonify, render_template,redirect, url_for, flash, session
from config import USERNAME, PASSWORD
from bbl.auth_manager import AuthManager
from bbl.playerinfo_manager import PlayerInfo_Manager
from bbl.matchinfo_manager import MatchInfoManager
from bbl.playerperformance_manager import Player_PerformanceManager
from bbl.teaminfo_manager import TeamInfo_Manager
from bbl.teamperformance_manager import TeamPerformanceManager


app = Flask(__name__)
app.secret_key = 'QWERTYUIOP'

# 数据库配置
db_url = "mongodb://localhost:27017/"
db_name = "BasketballDB"
player_manager = PlayerInfo_Manager(db_url, db_name)
team_manager = TeamInfo_Manager(db_url, db_name)
match_manager = MatchInfoManager(db_url, db_name)
######################################################################
@app.route('/')
def root():
    return render_template('root.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')

        # 尝试登录
        if AuthManager.login(username, password):
            return redirect(url_for('admin_dashboard'))  # 登录成功，跳转到管理员页面
        else:
            flash('账号或密码不匹配，请重新尝试！')  # 登录失败，显示提示信息
            return redirect(url_for('login'))  # 失败返回登录页面

    return render_template('login.html')


@app.route('/admin')
def admin_dashboard():
    # 确保只有已登录的用户可以访问管理员页面
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # 如果没有登录，跳转到登录页面
    return render_template('admin_dashboard.html')
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # 移除登录状态
    return redirect(url_for('login'))  # 登出后跳转到登录页面
####################################################################
@app.route('/manage_players')
def manage_players():
        players = player_manager.get_all_players()
        return render_template('manage_players.html', players=players)


# 查询球员
@app.route('/find_player', methods=['GET', 'POST'])
def find_player():
    player = None
    error = None

    if request.method == 'POST':
        player_id = request.form.get('player_id')
        player = player_manager.get_player_by_id(player_id)

        if not player:
            error = f"未找到 PlayerID 为 {player_id} 的球员。"

    return render_template('find_player_by_id.html', player=player, error=error)


# 球员详情
@app.route('/player/<player_id>')
def player_detail(player_id):
    player = player_manager.get_player_by_id(player_id)
    if not player:
        return f"未找到 PlayerID 为 {player_id} 的球员。"
    return render_template('player_detail.html', player=player)


# 修改球员信息
@app.route('/edit_player/<player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    player = player_manager.get_player_by_id(player_id)
    if not player:
        return f"未找到 PlayerID 为 {player_id} 的球员。"

    if request.method == 'POST':
        # 获取修改的数据
        updated_data = {
            "Name": request.form['Name'],
            "TeamID": request.form['TeamID'],
            "Number": request.form['Number'],
            "Position": request.form['Position']
        }
        player_manager.update_player(player_id, updated_data)
        return redirect(url_for('player_detail', player_id=player_id))

    return render_template('edit_player.html', player=player)


# 删除球员
@app.route('/delete_player/<player_id>', methods=['POST'])
def delete_player(player_id):
    player_manager.delete_player(player_id)
    return redirect(url_for('manage_players'))

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        try:
            # 获取表单数据
            player_data = {
                "PlayerID": request.form['PlayerID'],
                "Name": request.form['Name'],
                "TeamID": request.form['TeamID'],
                "Number": request.form['Number'],
                "Position": request.form['Position']
            }

            # 检查数据是否包含必要的字段
            required_fields = ['PlayerID', 'Name', 'TeamID', 'Number', 'Position']
            for field in required_fields:
                if field not in player_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            # 使用 player_manager 来添加球员
            player_manager.add_player(player_data)

            # 返回成功响应并重定向到球员管理页面
            return redirect(url_for('manage_players'))

        except Exception as e:
            return jsonify({"error": f"Failed to add player: {e}"}), 500

    return render_template('add_players.html')
#######################################################################################33
@app.route('/manage_teams', methods=['GET'])
def manage_teams():
    teams = team_manager.get_all_teams()
    # 渲染模板并传递查询到的球队信息
    return render_template('manage_teams.html', teams=teams)


@app.route('/team/<team_id>')
def team_detail(team_id):
    team = team_manager.get_team_by_id(team_id)
    if not team:
        return f"未找到 TeamID 为 {team_id} 的团队。"
    return render_template('team_detail.html', team=team)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():

    if request.method == 'POST':
        # 获取表单数据
        team_data = {
            "TeamID": request.form['TeamID'],
            "TeamName": request.form['TeamName'],
            "members": []
        }

        # 获取所有队员姓名和 ID
        members_name = request.form.getlist('members_name')  # 获取所有球员姓名
        members_id = request.form.getlist('members_id')      # 获取所有球员ID

        # 确保姓名和ID的数量匹配
        if len(members_name) != len(members_id):
            flash("球员姓名和球员ID数量不匹配", "error")
            return render_template('add_team.html')

        # 将成员信息整理成字典并添加到 `members` 列表中
        for i in range(len(members_name)):
            member = {
                "Name": members_name[i],
                "PlayerID": members_id[i]
            }
            team_data["members"].append(member)

        try:
            team_manager.add_team(team_data)  # 通过实例调用方法并传递参数
            flash("团队信息已成功添加", "success")
            return redirect(url_for('manage_teams'))  # 重定向回主页显示所有团队信息
        except ValueError as e:
            flash(str(e), "error")  # 如果发生错误，则显示错误信息

    # 渲染添加球队的页面
    return render_template('add_team.html')

#@app.route('/edit_team', methods=['GET', 'POST'])
@app.route('/edit_team/<team_id>', methods=['GET', 'POST'])
def edit_team(team_id=None):


    if team_id is None and request.method == 'POST':
        # 如果没有 team_id 参数，则从表单获取 team_id 进行查询
        team_id = request.form['TeamID']

    # 获取当前团队信息
    team = team_manager.get_team_by_id(team_id)  # 传递 team_id
    if not team:
        flash(f"未找到 TeamID 为 {team_id} 的团队。", "error")
        return render_template('edit_team.html', team=None, team_id=team_id)

    if request.method == 'POST':
        # 获取修改后的团队数据
        updated_data = {
            "TeamID": request.form['TeamID'],  # TeamID 通常是唯一的，不允许修改
            "TeamName": request.form['TeamName'],
            "members": []  # 新的成员列表
        }

        # 获取修改后的队员信息
        members_name = request.form.getlist('members_name')
        members_id = request.form.getlist('members_id')

        # 更新队员信息
        for name, player_id in zip(members_name, members_id):
            updated_data["members"].append({"Name": name, "PlayerID": player_id})

        # 调用业务逻辑层更新团队信息
        team_manager.update_team(team_id, updated_data)

        # 重定向到团队详情页
        return redirect(url_for('team_detail', team_id=team_id))

    # 渲染编辑团队页面
    return render_template('edit_team.html', team=team, team_id=team_id)

@app.route('/find_team_by_id', methods=['GET', 'POST'])
def find_team_by_id():
    team = None
    error = None

    if request.method == 'POST':
        team_id = request.form.get('team_id')
        team = team_manager.get_team_by_id(team_id)

        if not team:
            error = f"未找到 TeamID 为 {team_id} 的团队。"

    return render_template('find_team_by_id.html', team=team, error=error)
@app.route('/delete_team/<team_id>', methods=['POST'])
def delete_team(team_id):
    print(f"删除球队，TeamID: {team_id}")  # 调试输出
    team_manager.delete_team(team_id)
    return redirect(url_for('manage_teams'))
# 查询赛事
@app.route('/find_match', methods=['GET', 'POST'])
def find_match():
    match = None
    error = None

    if request.method == 'POST':
        match_id = request.form.get('match_id')
        match = match_manager.get_match_by_id(match_id)

        if not match:
            error = f"未找到 MatchID 为 {match_id} 的赛事。"

    return render_template('find_match_by_id.html', match=match, error=error)


# 赛事详情
@app.route('/match/<match_id>')
def match_detail(match_id):
    match = match_manager.get_match_by_id(match_id)
    if not match:
        return f"未找到 MatchID 为 {match_id} 的赛事。"
    return render_template('match_detail.html', match=match)


# 修改赛事信息
@app.route('/edit_match/<match_id>', methods=['GET', 'POST'])
def edit_match(match_id):
    match = match_manager.get_match_by_id(match_id)
    if not match:
        return f"未找到 MatchID 为 {match_id} 的赛事。"

    if request.method == 'POST':
        # 获取修改后的数据
        updated_data = {
            "MatchTime": request.form['MatchTime'],
            "Location": request.form['Location'],
            "Teams": [
                {
                    "TeamID": request.form.get('team1_id'),
                    "Name": request.form.get('team1_name'),
                    "Type": "Home",  # 假设 team1 是主队
                    "members": request.form.getlist('team1_members')
                },
                {
                    "TeamID": request.form.get('team2_id'),
                    "Name": request.form.get('team2_name'),
                    "Type": "Away",  # 假设 team2 是客队
                    "members": request.form.getlist('team2_members')
                }
            ],
            "Result": {
                "HomeScore": int(request.form['home_score']),
                "AwayScore": int(request.form['away_score']),
                "Winner": request.form['winner']
            },
            "Highlights": [
                {"Type": "Video", "URL": request.form.get('highlight_video_url')},
                {"Type": "Image", "URL": request.form.get('highlight_image_url')}
            ],
            "KeyEvents": {
                "Fouls": {
                    "HomeTeamFouls": int(request.form['home_fouls']),
                    "AwayTeamFouls": int(request.form['away_fouls'])
                },
                "Blocks": {
                    "HomeTeamBlocks": int(request.form['home_blocks']),
                    "AwayTeamBlocks": int(request.form['away_blocks'])
                },
                "Rebounds": {
                    "HomeTeamRebounds": int(request.form['home_rebounds']),
                    "AwayTeamRebounds": int(request.form['away_rebounds'])
                },
                "Steals": {
                    "HomeTeamSteals": int(request.form['home_steals']),
                    "AwayTeamSteals": int(request.form['away_steals'])
                }
            }
        }

        match_manager.update_match(match_id, updated_data)
        return redirect(url_for('match_detail', match_id=match_id))

    return render_template('edit_match.html', match=match)


# 删除赛事
@app.route('/delete_match/<match_id>', methods=['POST'])
def delete_match(match_id):
    match_manager.delete_match(match_id)
    return redirect(url_for('manage_matches'))



@app.route('/add_match', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        try:
            # 获取表单数据
            match_data = {
                "MatchID": request.form['MatchID'],
                "MatchTime": request.form['MatchTime'],
                "Location": request.form['Location'],
                "Teams": [
                    {
                        "TeamID": request.form.get('team1_id'),
                        "Name": request.form.get('team1_name'),
                        "Type": "Home",  # 假设 team1 为主队
                        "members": request.form.getlist('team1_members')
                    },
                    {
                        "TeamID": request.form.get('team2_id'),
                        "Name": request.form.get('team2_name'),
                        "Type": "Away",  # 假设 team2 为客队
                        "members": request.form.getlist('team2_members')
                    }
                ],
                "Result": {
                    "HomeScore": int(request.form['home_score']),
                    "AwayScore": int(request.form['away_score']),
                    "Winner": request.form['winner']  # "Home" 或 "Away"
                },
                "Highlights": [
                    {"Type": "Video", "URL": request.form.get('highlight_video_url')},
                    {"Type": "Image", "URL": request.form.get('highlight_image_url')}
                ],
                "KeyEvents": {
                    "Fouls": {
                        "HomeTeamFouls": int(request.form['home_fouls']),
                        "AwayTeamFouls": int(request.form['away_fouls'])
                    },
                    "Blocks": {
                        "HomeTeamBlocks": int(request.form['home_blocks']),
                        "AwayTeamBlocks": int(request.form['away_blocks'])
                    },
                    "Rebounds": {
                        "HomeTeamRebounds": int(request.form['home_rebounds']),
                        "AwayTeamRebounds": int(request.form['away_rebounds'])
                    },
                    "Steals": {
                        "HomeTeamSteals": int(request.form['home_steals']),
                        "AwayTeamSteals": int(request.form['away_steals'])
                    }
                }
            }

            # 检查数据是否包含必要的字段
            required_fields = ['MatchID', 'MatchTime', 'Location', 'Teams', 'Result']
            for field in required_fields:
                if field not in match_data:
                    flash(f"Missing required field: {field}", "error")
                    return redirect(url_for('add_match'))

            # 调试日志：打印 match_data 查看表单数据
            print(f"Match data received: {match_data}")

            # 使用 match_manager 来添加赛事
            match_manager.add_match_info(match_data)

            # 成功添加赛事
            flash(f"赛事 {match_data['MatchID']} 添加成功!", "success")
            return render_template('add_match.html', match_data=match_data)

        except Exception as e:
            # 输出异常详细信息
            print(f"Error occurred: {e}")
            flash(f"Failed to add match: {e}", "error")
            return redirect(url_for('add_match'))

    return render_template('add_match.html')

@app.route('/manage_matches')
def manage_matches():
    # 获取所有赛事信息
    matches = match_manager.get_all_matches()
    return render_template('manage_matches.html', matches=matches)


if __name__ == '__main__':
    app.run(debug=True)
