cat > Modelfile1 <<'EOF'
FROM gemma3:270m

PARAMETER temperature 1.0
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER num_predict 150
PARAMETER num_ctx 2048

SYSTEM """
You will answer in one line only.
"""
EOF