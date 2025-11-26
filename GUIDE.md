# 웹사이트 유지보수 가이드

이 가이드는 새로운 논문이나 연구 프로젝트가 있을 때 포트폴리오 웹사이트를 업데이트하는 방법을 설명합니다.

## 1. 새로운 논문(Publication) 추가하기

새로운 논문이 **Publications** 페이지와 **CV** 페이지 모두에 나타나도록 두 개의 파일을 업데이트해야 합니다.

### 단계 1: `_pages/publications.md` 업데이트
1.  `_pages/publications.md` 파일을 엽니다.
2.  해당하는 섹션을 찾습니다:
    *   **Journal Articles (Peer-reviewed)** (저널 논문)
    *   **Conference Proceedings & Presentations** (학회 발표)
3.  리스트의 맨 위에 새로운 논문을 다음 형식에 맞춰 추가합니다:
    ```markdown
    **Author1**; **Author2** (Year). "Title of the Paper." *Journal or Conference Name*. <a href="LINK_URL" class="external-link" title="View paper"><i class="fas fa-external-link-alt"></i></a>
    ```

### 단계 2: `_pages/cv.md` 업데이트
1.  `_pages/cv.md` 파일을 엽니다.
2.  **Publications** 섹션으로 이동합니다.
3.  해당하는 하위 섹션(**Working Papers**, **Selected Journal Articles**, 또는 **Selected Conference Proceedings**)에 논문을 추가합니다.
    *   *참고: CV 페이지는 강조하고 싶은 논문을 선택적으로 보여주기 위해 수동 리스트를 사용합니다.*

---

## 2. 새로운 연구 프로젝트(Research Project) 추가하기

### 단계 1: `_pages/research.md` 업데이트
1.  `_pages/research.md` 파일을 엽니다.
2.  **Current Projects** 또는 **Recent Projects** 섹션 아래에 새로운 프로젝트를 추가합니다:
    ```markdown
    **Project Title** (Year-Duration)
    *Funding Agency or Partner*
    Brief description of the project goals and your role.
    ```

### 단계 2: `_pages/cv.md` 업데이트
1.  `_pages/cv.md` 파일을 엽니다.
2.  **Current Research Projects** 섹션으로 이동합니다.
3.  기존 형식을 따라 프로젝트 내용을 추가합니다.

---

## 3. 변경 사항 미리보기 (로컬 테스트)

GitHub에 올리기 전에 내 컴퓨터에서 변경 사항을 확인하려면:

1.  터미널(PowerShell 또는 Command Prompt)을 엽니다.
2.  프로젝트 폴더로 이동합니다.
3.  다음 명령어를 실행합니다:
    ```powershell
    bundle exec jekyll serve
    ```
4.  웹 브라우저를 열고 주소창에 입력합니다: `http://localhost:4000`

> **참고:** `bundle install` 실행 시 "native extensions" 또는 `bigdecimal` 관련 오류가 발생하면 Ruby 개발 도구를 설치해야 할 수 있습니다. Conda를 사용 중이시므로 `conda install -c conda-forge compilers` 명령어로 컴파일러를 설치하거나 환경 설정을 확인해 보세요.
