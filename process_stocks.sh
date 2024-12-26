#!/bin/bash

# 종목 코드 리스트
stock_codes=("DHER.DE" "AAPL" "BAC" "BRK-B" "CAT" "JOBY" "MCD" "TSM" "AMZN" "GOOGL" "META" "MSFT" "NVDA" "TSLA")

# Pair 저장 배열
stock_date_pairs=()

# Pair 생성
for stock_code in "${stock_codes[@]}"; do
  if [ "$stock_code" == "DHER.DE" ]; then
    stock_date_pairs+=("$stock_code:2024-11-27")
  else
    stock_date_pairs+=("$stock_code:2024-12-02")
  fi
done

# Python 스크립트를 실행하여 처리
for pair in "${stock_date_pairs[@]}"; do
  # 종목 코드와 날짜 분리
  stock_code=$(echo "$pair" | cut -d':' -f1)
  donation_date=$(echo "$pair" | cut -d':' -f2)
  
  echo "Fetching data for $stock_code on $donation_date..."
  
  # Python 스크립트 실행
  python3 fetch_stock_data.py "$stock_code" "$donation_date"
done