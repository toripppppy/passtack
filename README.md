# Passtack
Stack and pass and attack the path!

# ゲームルール
Passtackは一対一で戦うターン制のコマンドバトルです。  
１ゲームは５ターン。５ターン分のコマンドをゲーム開始前に決定して勝負に挑みます。  
相手が用意してくる手をよく推察して、より多く相手を攻撃しよう！

### 勝利条件
より多く相手に攻撃すること。  
HPのような概念は無く、攻撃できた回数を競います。
### コマンド
コマンドは全部で５種類。それぞれのコマンドには「サイン」と呼ばれる記号が存在します。  
また、それぞれのコマンドには必要ターンがあるので、全部で５ターンになるように計算して手を組む必要があります。  
詳しくは下のコマンド一覧を参照。
### スタック
手元に用意した５ターン分（５個とは限らない）のコマンドのことを「スタック」と呼びます。


## コマンド一覧
- 【 . 】攻撃（必要ターン：１）  
  相手に１ダメージ分攻撃する。
  
- 【 , 】大攻撃（必要ターン：２）  
  １ターン目、相手に２ダメージ分攻撃する。
  ２ターン目は休憩する。
  
- 【 * 】集中（必要ターン：２）  
  １ターン目、集中することで、相手の次のターンのコマンドを確認できる。  
  また、コマンドを確認した上で自分の２ターン目の行動を選択することができる。  
  確認したコマンドが「大攻撃（２ターン目）」だった場合、何もない未来を読んだショックで２ターン目は休み。
  
- 【 _ 】トラップ（必要ターン：１）  
  相手のコマンドが「大攻撃」の時、跳ね返すことができる。（相手に２ダメージ分攻撃する。）
  
- 【 ? 】推理（必要ターン：１） 
  相手のコマンドを推理する。  
  もし推理が的中すれば、相手のコマンドをキャンセルして、相手に１ダメージ分攻撃できる。  
  相手のコマンドが「攻撃」の時、見え見えなので必ず的中させられる。  
  相手のコマンドが「集中」の時、攻撃はするがキャンセルはしない。

### スタック表記
スタックを表す際に、コマンドのサインを「/」で区切って　`./,/_/.` のように表記できます。  
