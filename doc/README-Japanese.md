# Texts比較ツール
<p align="center">
  <img src='../images/logo.png' width=300>
</p>

<p align="center">
    【<a href="../doc/README-English.md">英語</a> | <a href="../doc/README-Chinese.md">中文</a> | 日本語】
</p>

## 📖 概要

このツールはテキスト比較に使用されます。類似した2つのテキスト間の違いを迅速に識別し、テキストの比較作業を簡単かつ効率的に行うのに役立ちます。

---

### サンプル 1

#### 入力

| テキスト A | テキスト B |
| --- | --- |
| Today is a good weather day | Today is a bad weather day |

#### 出力

`Excel` として出力：

<p align="center">
  <img src='../images/example_1.jpg' width=600>
</p>

`JSON` として出力：
```json
{
    "0": {
        "left": {
            "text": "Today is a good weather day",
            "red_marks": [11, 12, 13],
            "tag": "Index 1"
        },
        "right": [
            {
                "text": "Today is a bad weather day",
                "red_marks": [11, 12],
                "tag": "Index 1"
            }
        ]
    }
}
```

---

### サンプル 2

#### 入力

<table>
  <tr>
    <th>テキスト A</th>
    <th>テキスト B</th>
  </tr>
  <tr>
    <td rowspan="3">Let me not to the marriage of true minds<br>Admit impediments. Love is not love<br>Which alters when it alteration finds,<br>Or bends with the remover to remove:<br>O, no! it is an ever-fix`ed mark,<br>That looks on tempests and is never shaken;<br>It is the star to every wand'ring bark,<br>Whose worth's unknown, although his heighth be taken.<br>Love's not Time's fool, though rosy lips and cheeks<br>Within his bending sickle's compass come;<br>Love alters not with his brief hours and weeks,<br>But bears it out even to the edge of doom:<br>If this be error and upon me proved,<br>I never writ, nor no man ever loved.</td>
    <td>Let me not to the marriage of true minds<br>Admit impediments. Love is not love<br>Which alters when it alteration finds,<br>Or bends with the remover to remove:<br>O, no! it is an ever-fix`ed mark,<br>That looks on tempests and is never shaken;</td>
  </tr>
  <tr>
    <td>It is the star to every wand'ring bark,<br>Whose worth's unknown, although his heighth be taken.<br>Love's not Time's fool, though rosy lips and cheeks</td>
  </tr>
  <tr>
    <td>Within his bending sickle's compass come;<br>Love alters not with his brief hours and weeks,<br>But bears it out even to the edge of doom:<br>If this be error and upon me proved,<br>I never writ, nor no man ever loved.</td>
  </tr>
</table>

#### 出力

`Excel` として出力：

<p align="center">
  <img src='../images/example_2.jpg' width=600>
</p>

`JSON` として出力：
```json
{
    "0": {
        "left": {
            "text": "Let me not to the marriage of true minds\nAdmit impediments. Love is not love\nWhich alters when it alteration finds,\nOr bends with the remover to remove:\nO, no! it is an ever-fix`ed mark,\nThat looks on tempests and is never shaken;\nIt is the star to every wand'ring bark,\nWhose worth's unknown, although his heighth be taken.\nLove's not Time's fool, though rosy lips and cheeks\nWithin his bending sickle's compass come;\nLove alters not with his brief hours and weeks,\nBut bears it out even to the edge of doom:\nIf this be error and upon me proved,\nI never writ, nor no man ever loved.",
            "red_marks": [4, 5, 27, 28, 241, 242, 243, 244, 343, 344, 345, 346, 413, 414, 415, 416, 496, 497, 498, 499, 518, 519],
            "tag": "Index 1"
        },
        "right": [
            {
                "text": "Let ## not to the marriage ## true minds\nAdmit impediments. Love is not love\nWhich alters when it alteration finds,\nOr bends with the remover to remove:\nO, no! it is an ever-fix`ed mark,\nThat looks on tempests and is never shaken;", 
                "red_marks": [4, 5, 27, 28], 
                "tag": "Index 1"
            },
            {
                "text": "It is the #### to every wand'ring bark,\nWhose worth's unknown, although his heighth be taken.\nLove's not Time's ####, though rosy lips and cheeks", 
                "red_marks": [10, 11, 12, 13, 112, 113, 114, 115], 
                "tag": "Index 2"
            },
            {
                "text": "Within his bending sickle's compass ####;\nLove alters not with his brief hours and weeks,\nBut bears it out even to the #### of doom:\nIf this ## error and upon me proved,\nI never writ, nor no man ever loved.", 
                "red_marks": [36, 37, 38, 39, 119, 120, 121, 122, 141, 142], 
                "tag": "Index 3"
            }
        ]
    }
}
```

---

## 👨‍💻‍ 貢献者

<a href="https://github.com/VintLin/texts-comparator/contributors">
  <img src="https://contrib.rocks/image?repo=VintLin/texts-comparator" />
</a>

[contrib.rocks](https://contrib.rocks)で作成されました。

## ⚖️ ライセンス

- ソースコードライセンス: 当プロジェクトのソースコードはMITライセンスの下でライセンスされています。このライセンスにはMITライセンスの指定条件が含まれており、コードの使用、変更、配布が許可されています。
- プロジェクトのオープンソースステータス: このプロジェクトは確かにオープンソースですが、この指定は主に非営利目的を意図しています。コミュニティからの研究および非商用アプリケーションへの協力と寄付を奨励していますが、プロジェクトのコンポーネントを商業目的で利用する場合、別途ライセンス契約が必要です。

## 🌟 スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=VintLin/texts-comparator&type=Date)](https://star-history.com/#VintLin/texts-comparator&Date)

## 📬 お問い合わせ

質問、フィードバック、またはお問い合わせがある場合は、[vintonlin@gmail.com](mailto:vintonlin@gmail.com) までお気軽にお問い合わせください。
