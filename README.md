# 이 프로젝트에 대해서

> 이 프로젝트는 Pygame 을 통해 간단한 게임 화면을 띄우는 목적으로 개발 되고 있음   
Assets 은 온라인에서 Free License 를 구했으며 연습용으로 개발되고 있음을 알림

* * *

# [코드 설명]

## core.py

### - *Class: BaseGame*

    작성할 게임들은 BaseGame 클래스를 꼭 상속 하고 있어야 한다
    BaseGame 클래스 내에 update() 함수를 통해 pygame 의 기본적인 템플릿을 구현하고 있기 때문

### - *Class: GameComponent*

    BaseGame 을 상속받은 게임기본 클래스 내에 선언이 기본이며 show(), fill() 등 pygame 에서 기본적으로 컨트롤이 필요하거나 자주 쓰일만한 함수들을 미리 지정해놓고 사용 할 수 있게 만든것이 목표

### - *Class: KeyBindings - static class*

    키와 관련 된 bool 메소드 들을 하나의 클래스 내에 묶어 놓음 GameModel 내에 Key Event 들을 정리할 예정이라 불가피하게 소스가 길어지는것을 최대한 막기 위해 static methods 로
    관리하기로 했음

* * *

# 개발 시작일

* 21.03.06*
