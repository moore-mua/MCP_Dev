FROM ubuntu:24.04

# 作業ディレクトリを作成
WORKDIR /workspace

# git や curl 等の最低ツールを入れる
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl ca-certificates git \
    nodejs npm \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh


# Codex CLI をグローバルにインストール
RUN npm install -g @openai/codex



# コンテナ起動時に bash（または sh）を起動（対話モード）
CMD ["bash"]