# LstmSongGen
## インストールが必要なパッケージ
- mido
- keras

## セットアップ
- 走らせる前にrun.shの中身を変更してください
```sh
  3 INPUT_DIR=testInput/   #入力するmidiデータを格納したディレクトリ名（パス付き）
  4 OUTPUT=output          #"入力した名前"+result.mid がAI が予測した音楽出力です
  5 MODEL_NAME=test_model  #モデルの名前です。もし同じ名前のモデルが既にある場合に./run.sh を行った場合、新たに作成せずに既存のものを使って予測します。
  6 BPM="120"              #手動で出力曲のbpm を決めます。
```

## 走らせ方
```
<!--on terminal-->
$ ./run.sh
```

## 備考
- main.py の中にdiversity というものがあるのですが、この値を上げれば上げるほど、確率の低いものをあえて取ってくる頻度が高くなるみたいです。今の所0.2 と低めに設定しています。
