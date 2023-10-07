from flask import Flask, render_template, request
import re
import os

app = Flask(__name__)

DISCORD_PERMISSIONS = {
    "CREATE_INSTANT_INVITE": 0x00000001,
    "KICK_MEMBERS": 0x00000002,
    "BAN_MEMBERS": 0x00000004,
    "ADMINISTRATOR": 0x00000008,
    "MANAGE_CHANNELS": 0x00000010,
    "MANAGE_GUILD": 0x00000020,
    "ADD_REACTIONS": 0x00000040,
    "VIEW_AUDIT_LOG": 0x00000080,
    "PRIORITY_SPEAKER": 0x00000100,
    "STREAM": 0x00000200,
    "VIEW_CHANNEL": 0x00000400,
    "SEND_MESSAGES": 0x00000800,
    "SEND_TTS_MESSAGES": 0x00001000,
    "MANAGE_MESSAGES": 0x00002000,
    "EMBED_LINKS": 0x00004000,
    "ATTACH_FILES": 0x00008000,
    "READ_MESSAGE_HISTORY": 0x00010000,
    "MENTION_EVERYONE": 0x00020000,
    "USE_EXTERNAL_EMOJIS": 0x00040000,
    "VIEW_GUILD_INSIGHTS": 0x00080000,
    "CONNECT": 0x00100000,
    "SPEAK": 0x00200000,
    "MUTE_MEMBERS": 0x00400000,
    "DEAFEN_MEMBERS": 0x00800000,
    "MOVE_MEMBERS": 0x01000000,
    "USE_VAD": 0x02000000,
    "CHANGE_NICKNAME": 0x04000000,
    "MANAGE_NICKNAMES": 0x08000000,
    "MANAGE_ROLES": 0x10000000,
    "MANAGE_WEBHOOKS": 0x20000000,
    "MANAGE_EMOJIS": 0x40000000
}

def decode_permissions(permissions_bitmask):
    granted_permissions = []
    for perm_name, perm_value in DISCORD_PERMISSIONS.items():
        if permissions_bitmask & perm_value:
            granted_permissions.append(perm_name)
    return granted_permissions

@app.route('/', methods=['GET', 'POST'])
def index():
    permissions_list = []
    link = ""

    if request.method == 'POST':
        link = request.form.get('link')
        permissions_value = extract_permissions_bitmask(link)
        if permissions_value is not None:
            permissions_list = decode_permissions(permissions_value)

    return render_template('index.html', permissions=permissions_list, link=link)

def extract_permissions_bitmask(link):
    match = re.search(r'permissions=(\d+)', link)
    if match:
        return int(match.group(1))
    return None

if __name__ == '__main__':
    repl_id = os.getenv('REPL_ID')
    if repl_id:
        print(f"Your app is live at: https://DiscordBotInviteLinkPermsChecker.{repl_id}.repl.co")
    app.run(host='0.0.0.0', port=5000)
