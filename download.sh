#!/bin/bash

# 下载目录
OUTPUT_DIR="/Users/andrew/movies/跃动青春"
mkdir -p "$OUTPUT_DIR"

# 格式: "URL|集数名"
urls=(
  "https://vip.dytt-hot.com/20250128/21847_d140b46b/index.m3u8|第四集"
  "https://vip.dytt-hot.com/20250128/21844_31f0a067/index.m3u8|第五集"
  "https://vip.dytt-hot.com/20250128/21861_d29ac33c/index.m3u8|第六集"
  "https://vip.dytt-hot.com/20250128/21851_fe39765e/index.m3u8|第七集"
  "https://vip.dytt-hot.com/20250128/21869_a2009556/index.m3u8|第八集"
  "https://vip.dytt-hot.com/20250128/21867_8854e852/index.m3u8|第九集"
  "https://vip.dytt-hot.com/20250128/21871_460eb45f/index.m3u8|第十集"
  "https://vip.dytt-hot.com/20250128/21875_4849ef4e/index.m3u8|第十二集"
)

for entry in "${urls[@]}"; do
  url="${entry%%|*}"
  name="${entry##*|}"
  echo "========================================="
  echo "开始下载 ${name}..."
  echo "========================================="
  yt-dlp -o "${name}.mp4" \
    -P "$OUTPUT_DIR" \
    --add-header "Origin: https://art.v2player.top:8989" \
    --add-header "Referer: https://art.v2player.top:8989" \
    --add-header "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36" \
    --downloader aria2c \
    --downloader-args "aria2c:-x 8 -s 8 -k 1M" \
    "$url"
  
  if [ $? -eq 0 ]; then
    echo "✅ ${name} 下载完成！"
  else
    echo "❌ ${name} 下载失败，请检查网络或链接是否有效"
  fi
  echo ""
done

echo "========================================="
echo "🎉 全部下载完成！"
echo "========================================="