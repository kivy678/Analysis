<style>
	body {
		font-family: Hack;
		font-size  : 1.3em;	
	}
	span {
		font-family: 나눔바른고딕;
	}
</style>


# <span>안드로이드 분석 툴</span>
# <span>v1.0.0</span>

---

## <span>개요</span>
<span>
악성, 모딩 앱을 쉽게 분석 할 수 있도록 지원하는 안드로이드 분석 툴입니다. </br>
자동화를 추가할 예정입니다. </br>
</span>
소개 영상: https://youtu.be/


## <span>요구 사양</span>
| 시스템 / 환경 | 값 |
| :----------: | -- |
| OS | Windows, Linux(에뮬레이터 불가) |
| 언어 | Python3.7 / C |
| 웹 | Flask, Redis |
| 디컴파일러 | apktool, Jadx, 안드로가드, [Il2cppdumper], [JustDecompile] |
| 데이터 프레임 | pandas |
| 데이터 분석 | 스파크, 엘라스틱 서치, 키바나 |


## <span>내장 툴 크로스 컴파일</span>
1. [Android NDK]를 다운로드

2. 안드로이드 툴 체인 생성 	</br>
`$ python3 android-ndk-r21b/build/tools/make_standalone_toolchain.py --arch x86  --api 24  --install-dir=my-toolchain`

3. 크로스 컴파일 	※ i686=32bit x86_64=64bit </br>
`$ my-toolchain/bin/clang -o my-tool my-tool.c`

4. API22 부터 링커 경고가 뜨는데 이를 제거
```
$ git clone https://github.com/termux/termux-elf-cleaner.git
$ make
$ termux-elf-cleaner <filenames>
```

## <span>내장 툴 크로스 컴파일 (dockcross) </span>
1. dockcross 다운  </br>
`$ docker pull dockcross/linux-x86`
2. dockcross 를 이용한 크로스 컴파일  </br>
`$ docker run --rm -v /root/data:/work dockcross/linux-x86 bash -c 'my-toolchain/bin/clang -o my-tool my-tool.c'`


## <span>설치</span>
1. 파이썬 가상화  </br>
`$ virutalenv .env --python=python3`
2. 파이썬 가상화 실행  </br>
`$ .env\\Script\\activate.bat`
3. 파이썬 모듈 빌드  </br>
`(.env) $ python setup.py install`
4. 추가 모듈 설치  </br>
`(.env) $ pip3 install -r requirements.txt`
5. 가상화 끄기  </br>
`(.env) $ deactivate`

## <span>실행</span>
1. 환경 패스 설정  </br>
`$ vi global.ini`
2. 엘라스틱서치와 레디스 서버가 설치되어 있다면 설정  </br>
`$ vi webConfig.py`
3. 환경 패스 초기화  </br>
`$ python initialize.py -i`
4. 웹 서버 구동  </br>
`$ python server.py -p [port]`


## <span>사용</span>
1. work/sample 에 샘플을 넣는다.
2. 기본 분석을 진행한 뒤, 분석할 샘플을 선정한다.




[Android NDK]: https://developer.android.com/ndk/downloads?hl=ko
[Il2cppdumper]: https://github.com/Perfare/Il2CppDumper
[JustDecompile]: https://www.telerik.com/products/decompiler.aspx
