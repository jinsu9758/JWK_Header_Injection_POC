# JWK Header Injection


## 취약점 개요
서버에서 JWT 검증 시, Header에 포함된 JWK를 신뢰하는 경우 취약점이 발생   


----

## 환경 설정
`git clone https://github.com/jinsu9758/JWK_Header_Injection_POC.git`  

`sudo docker build -t jwk-header-injection .`  

`sudo docker run -p 5000:5000 jwk-header-injection`  

※ 5000번 포트로 접속 가능

----

## 공격 수행 과정
https://blog.naver.com/jinsu9758/223823960983
