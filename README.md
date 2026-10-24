# 関ヶ原の戦い / Battle of Sekigahara — 1600

Blender＋Python＋FFmpegだけで生成する、縦型の簡易3D戦略ゲーム風動画。
720×1280 / 9:16 / 30fps / 2100フレーム / 70秒。ナレーションなし。
赤＝西軍、青＝東軍。上下に短い日本語・英語字幕を焼き込みます。

## 制作段階

- Part 1: `scene.py` の地形・中山道の模式図・布陣・俯瞰カメラ。
- Part 2: 同ファイルの進軍・迎撃・激突・旗・煙・寝返り・敗走・カメラ移動。
- Part 3: `produce.py` の字幕、オリジナル合成音響、FFmpegによるMP4化とActions。

Part 1・2はシーンを保存するだけで、`--render` 指定時に初めてレンダリングします。
煙は軽量なポリゴン表現です。無料のWorkbenchを使用しGPUを必須にしません。

## ローカル実行

Blender 4.x、Python 3、FFmpeg（libass / libx264対応）、Noto CJKフォントが必要です。
Ubuntu 24.04:

```sh
sudo apt-get update
sudo apt-get install -y blender ffmpeg fonts-noto-cjk
# 地形・布陣・アニメーションを構築して保存。レンダリングしない
blender -b --python scene.py
# 最終フレームを全てレンダリング
blender -b -t 4 --python scene.py -- --render
# 音響生成・字幕焼き込み・MP4統合
python3 produce.py
ffprobe -v error -show_streams -show_format build/sekigahara.mp4
```

完成品: `build/sekigahara.mp4`。編集用: `build/sekigahara.blend`。
中間フレームは `build/frames/frame_0001.png` ～ `frame_2100.png`。
`--out build` は両スクリプトで指定可能です。
失敗した範囲のみ `--render --start 301 --end 600` で再生成できます。
`produce.py` は2100枚が揃った後に実行してください。欠損・破損時はレンダリングを再実行します。

## GitHubから完成動画を取得

1. **Actions → Render Sekigahara → Run workflow → main → Run workflow**。
   対象ファイルのmainへのpushでも自動実行します。
2. 完了した実行の **Artifacts → sekigahara-720x1280-30fps** をダウンロード。
3. ZIP内の `build/sekigahara.mp4` が完成動画です。Artifactsは30日保存します。

生成成功後は `video-コミットSHA先頭12桁` のReleaseを自動作成し、MP4を添付します。
既存の公開Releaseを作成した場合も同ワークフローでMP4を添付します。
Releasesへの書き込みが制限されている場合も、成功済みのArtifactsから取得できます。Actions無効・利用枠超過時は
Settings → Actionsを確認するかローカル実行してください。
レンダリングにはCPU性能に応じて時間と中間画像用ディスクが必要です。
エラー時は失敗ステップのログを開き、修正後 **Re-run failed jobs**。
このREADMEの取得手順はワークフローの仕様です。実行成功はActionsの緑の結果で確認してください。

## 時間構成

| 秒 | 映像・字幕・音響 |
|---|---|
| 0–3 | 両軍を近くから見せる導入、太鼓と低音 |
| 3–15 | 俯瞰へ引き、両軍の布陣と色分け、簡略再現の注記 |
| 15–35 | 東軍進軍と西軍迎撃、行軍の打音 |
| 35–55 | 激突、旗と煙、打撃ノイズ |
| 55–62 | 小早川の西軍攻撃、音程変化の合図 |
| 62–67 | 西軍敗走、速い足音風の効果 |
| 67–70 | 「関ヶ原の戦い 1600年 / Battle of Sekigahara」と注記、音響フェード |

## 史実と簡略化

慶長5年9月15日（グレゴリオ暦1600年10月21日）の戦いが題材です。
北を+Y、東を+Xとし、石田三成を笹尾山側の北西、宇喜多・小西を西側、
大谷を南西、小早川を松尾山側の南西、徳川家康を東側に配置しています。
福島、井伊・松平、黒田・細川は東軍の模式的な部隊です。

**史実を簡略化した再現です。** 地形・道路・縮尺・部隊数・軌跡は測量データや
厳密な戦況復元ではありません。70秒は実際の経過時間ではありません。
布陣の細部や小早川の参戦時刻・経緯には研究上の議論があり、通説的な展開を
映像向けに圧縮しています。「家康の問鉄砲」は断定して描いていません。
小早川隊は当初の所属を示す赤い旗のまま西軍を攻撃します。

参考となる公的な解説先（細部の学術的確定を意味しません）:
- 岐阜関ケ原古戦場記念館: https://sekigahara.pref.gifu.lg.jp/
- 関ケ原観光ガイド: https://www.sekigahara1600.com/

## 音源とライセンス

外部の音源素材を使わずPythonでオリジナルBGMと効果音を生成します。
商用利用可能なCC0として公開する条件・出所・ツールの条件は
[AUDIO_LICENSE.md](AUDIO_LICENSE.md) を参照してください。
