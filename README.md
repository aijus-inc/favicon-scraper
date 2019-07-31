# favicon-scraper
このプロジェクトは、Hubspotの情報を自動的に補完する処理を行うためのものです。

## 環境情報(開発時の環境)

- python 2.7.10
- pip 19.2.1
- pipenv (version 2018.11.26)

## パッケージのインストール
```$ pipenv install```  
で必要なパッケージをpipenv上の仮想環境にインストールします。

## 準備
const.pyを開き、  
apikey = '0fa59160-94cb-40ad-85fe-e7678c23f46f'
の部分を、使用するアカウントに合わせて書き換えてください。

参考：[HubSpot APIキーへのアクセス](https://knowledge.hubspot.com/jp/articles/kcs_article/integrations/how-do-i-get-my-hubspot-api-key)


## 実行コマンド
```$ pipenv run favicon```  
 --> faviconの保存  
 各ドメインを参照して取得したfaviconを、ローカルファイルとして/faviconsフォルダに保存します

```$ pipenv run start```  
 --> 住所の取得  
各ドメインからサイトトップページにアクセス。  
「会社概要」や「アクセス」のリンクを辿りながら、正規表現で住所と予想できるデータを取得し、ローカルにaddress_list.csvとして保存します  
※途中、totarotanaka.comからusernameとpassを求められ、処理が止まります。control+cなどで入力をスキップしてください。(解決方法がわかりませんでした)


## オプション
```$ pipenv run show```  
ドメイン一覧を配列に近い形式でprintします。

```$ pipenv run reset```  
会社一覧を初期化します（テスト環境構築用）  
絶対に本番環境で使用しないこと  
※使用時はconst.pyから「production_mode = False」にし、十分気をつけて実行してください。  

## 開発メモ
hubspotテスト用アカウントおよびユーザー  
https://app.hubspot.com/contacts/6181502/companies/list/view/all/?  
user: ryosui.yamagata@nadai.jp  
pass: nci1201LL  

## 引き継ぎメモ
 - faviconについて  
  - Hubspotには、会社のアイコンを更新するAPIは存在しないかもしれない。  
  - 16*16pxの画像でよければ、googleのAPI（https://www.google.com/s2/favicons?domain= ）を使って取得できる。ただしドメイン名にwww.が必要だったり余分だったりする。  
  - アイコンが設定済みかどうかは、hs_avatar_filemanager_keyを参照すればわかるが、Hubspotによる自動設定のアイコンはこの限りではない。（func.pyコメントアウト部分に残骸を残している）  
 - 住所取得について  
  - 全自動でやれるほど精度を高められなかったため、候補データは全て保存する方式にした。
  - 住所を取得した際に、ゴミが混じることがある。（ex.○○県○○市でイベントを行います）
  - 大企業では、会社概要ページに本社の住所と支社の住所が同時に載っていることがよくある。（本社という文字列を参照すべき？）
  - 住所データが設定済みかどうかは、Hubspotのapiから参照できそう。
  - 住所データの更新も、Hubspotのapiから参照できそう。
