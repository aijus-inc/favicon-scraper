# favicon-scraper
このプロジェクトは、Hubspotの情報を自動的に補完する処理を行うためのものです。

## 環境情報(開発時の環境)
python 2.7.10
pip 19.2.1
pipenv (version 2018.11.26)

## パッケージのインストール
$ pipenv install
で必要なパッケージをpipenv上の仮想環境にインストールします。

## 準備
const.pyを開き、
apikey = '0fa59160-94cb-40ad-85fe-e7678c23f46f'
の部分を、使用するアカウントに合わせて書き換えてください。

参考：[HubSpot APIキーへのアクセス](https://knowledge.hubspot.com/jp/articles/kcs_article/integrations/how-do-i-get-my-hubspot-api-key)


## 実行コマンド
$ pipenv run start
 - 住所の取得(実装中)
$ pipenv run favicon
 - faviconの保存

## 行われる処理
pipenv上の仮想環境で以下の処理を実行します。
・company（会社）一覧に対してアイコンが設定されていないものを検出し、各ドメインからfaviconを取得して設定します。
 - apiの関係上実装できなかったため、ローカルファイルとしてfaviconを保存します。
・company（会社）一覧に対して住所が設定されていないものを検出し、各ドメインから住所を取得して設定します。
 - 実装中です。

## オプション
$ pipenv run show
ドメイン一覧を配列に近い形式でprintします。
$ pipenv run reset
会社一覧を初期化します（テスト環境構築用）
絶対に本番環境で使用しないこと
※使用時はconst.pyから「production_mode = False」にし、十分気をつけてください。
