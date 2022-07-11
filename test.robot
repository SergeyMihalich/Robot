*** Settings ***
Library  one.py
Library  WorkRobot.py


*** Variables ***
${username}     FSM_VLG
${password}     Pass1230
${message_id}       id=t3_vuixro
${comment}      1234567890Testing
${url_token_temporary}      https://www.reddit.com/account/sso/one_tap/?experiment_d2x_2020ify_buttons=enabled&experiment_d2x_sso_login_link=enabled&experiment_d2x_google_sso_gis_parity=enabled&experiment_d2x_onboarding=enabled
${url_login}      https://www.reddit.com/login
${url_my_token}      https://www.reddit.com/
${url_write_message}      https://oauth.reddit.com/api/comment.json?rtj=only&emotes_as_images=true&redditWebClient=desktop2x&app=desktop2x-client-production&raw_json=1&gilding_detail=1
${url_del_message}      https://oauth.reddit.com/api/del?redditWebClient=desktop2x&app=desktop2x-client-production&raw_json=1&gilding_detail=1
${url_check_message}   https://www.reddit.com/user/FSM_vlg/





*** Test Cases ***
Do a GET Request session
    Login       ${username}     ${password}     ${url_token_temporary}  ${url_login}
    Write Message       ${message_id}       ${comment}  ${url_write_message}    ${url_my_token}
    Check Write Message     ${url_check_message}        ${comment}
    Del Message     ${message_id}   ${url_del_message}  ${url_my_token}
    Check Del Message     ${url_check_message}        ${comment}

*** Keywords ***
