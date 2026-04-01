# 共通テスト自動採点・講評システム デプロイ手順

Streamlitアプリケーションのデプロイには、無料で簡単に構築ができる **Streamlit Community Cloud** が一番おすすめです。
デプロイに向けて、APIキーが含まれた `.env` などの機密ファイルが誤って公開されないよう、リポジトリ内に新しく `.gitignore` ファイルを作成しておきました。

以下に、数分で完了するデプロイ手順をまとめました。

## 1. コードをGitHubにプッシュする
まずは、現在の開発フォルダ（`c:\Projects\common_test_reviewer`）をGitリポジトリにして、ご自身のGitHubアカウントにプッシュしてください。
※ `GEMINI_API_KEY` を書いた `.env` ファイルは、`.gitignore` で除外されているためGitHubには公開されません（安全です）。

## 2. Streamlit Cloud にログイン
👉 [Streamlit Community Cloud](https://share.streamlit.io/) にアクセスし、GitHubアカウント連携でログインします。

## 3. 新しいアプリを作成 (New app)
画面右上の `New app` をクリックし、「Use existing repo」から以下の設定を行います。
- **Repository**: さきほど作成したGitHubリポジトリを選択
- **Branch**: `main`（または `master`）
- **Main file path**: `app.py`

## 4. APIキー（Secrets）を安全に設定する
これは非常に重要です。Deployボタンを押す前に **「Advanced settings」** （または設定内の **Secrets** ）を開き、ローカルの `.env` と同じようにキーを登録します（形式はTOMLになります）。

```toml
GEMINI_API_KEY="AIzaSy...（ご自身のAPIキーに置き換えてください）"
```

## 5. デプロイ実行
「Deploy」ボタンを押すと、自動的にサーバー側で `requirements.txt` が読み込まれて環境が構築され、数分でアプリが世界中に公開されます！🎉
