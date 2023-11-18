# video-dl

Webページからビデオをダウンロードするスクリプト

### python version

```
[requires]
python_version = "3.8"
```


### dependencies(pipenv and pyenv required)

```
pipenv shell
```

### usage 

```
python main.py -b https://www.example.com/users -u 100000
```

### options

```
options:
  -h, --help            show this help message and exit
  --base_url BASE_URL, -b BASE_URL
                        ベースとなるURL
  --user_id USER_ID, -u USER_ID
                        ユーザーID
  --start_page START_PAGE, -s START_PAGE
                        開始ページ
  --end_page END_PAGE, -e END_PAGE
                        終了ページ
  --download_directory DOWNLOAD_DIRECTORY, -d DOWNLOAD_DIRECTORY
                        ダウンロードするディレクトリ
  --no_headless         非ヘッドレスモードで実行（デフォルトは無効）
```