#!/bin/sh
# author: 🐖^(*￣(oo)￣)^

#你自己的refresh_token
refresh_token="${REFRESH_TOKEN}"
pig_url="${PIG_URL}"
pig_username="${PIG_USERNAME}"
pig_password="${PIG_PASSWORD}"
refresh_token="297e63b67e9e42d18925190e540ec8a0"

header="Content-Type: application/json"
login_ali_cloud_drive(){
  local url=$1
  local body='{ "grant_type": "refresh_token", "refresh_token": "'"$refresh_token"'" }'
  response=$(curl -s -X POST "$url" -H "$header" -H "Authorization: $refresh_token" -d "$body")

  local access_token=$(echo $response | grep -ioP '(?<="access_token":").*?(?=",)')
  echo $access_token
}
checkin_ali_cloud_drive(){
  local url=$1
  local access_token=$2
  local body='{"grant_type": "refresh_token", "refresh_token": "'$refresh_token'"}'
  sign=$(curl -s -X POST "$url" -H "$header" -H 'Authorization:Bearer '$access_token'' -d "$body" )

  success=$(echo $sign | grep -ioP '"success":.*?[,}]')
  title=$(echo $sign | grep -ioP '"title":.*?[,}]')
  subject=$(echo $sign | grep -ioP '"subject":.*?[,}]')

  signInCount=$(echo $sign | grep -ioP '(?<="signInCount":).*?(?=[,"}])')
  signInCover=$(echo "$sign" | grep -ioP '"signInCover":.*?[,}]')
  # 输出 $title $subject $signInCover 值
  echo "$title $subject $signInCover"

  if [[ -z "$title" || "$success" != '"success":true,' ]]; then
    code=$(echo "$sign" | grep -o '"code": *"[^"]*"' | sed 's/"code": *"\([^"]*\)"/\1/')
    message=$(echo "$sign" | grep -o '"message": *"[^"]*"' )
    echo "错误！！！：code: $code, $message"
  else
    echo "签到执行状态： $success 你已经签到： $signInCount "
  fi
}
ali_cloud_drive(){
  access_token=$(login_ali_cloud_drive "https://auth.aliyundrive.com/v2/account/token")
  #echo $access_token
  result=$(checkin_ali_cloud_drive "https://member.aliyundrive.com/v1/activity/sign_in_list" $access_token)
  echo $result
}
#ali_cloud_drive


login_pig(){
#  local url=$1
  response=$(curl 'https://dir.tianwen.monster/auth/login' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'cookie: ip=e0cf9225b5f272719aed3aff662cc5db; expire_in=1728797765' \
  -H 'origin: https://dir.tianwen.monster' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://dir.tianwen.monster/auth/login' \
  -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'email=qingdoor%40outlook.com&passwd=1&code=')

  echo $response
}
#checkin_pig(){}
pig_large_aircraft(){
  login_pig_resutl=$(login_pig "https://dir.tianwen.monster/auth/login" )
  echo $login_pig_resutl
  #result=$(checkin_pig "https://member.aliyundrive.com/v1/activity/sign_in_list" $access_token)
  #echo $result
}
#pig_large_aircraft