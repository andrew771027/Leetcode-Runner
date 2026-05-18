# LeetCode Runner

1. 使用python內建的argparse做cli
2. 使用subprocess去執行另一個repo的測試code，會遇到要使用哪個repo的portry virtual environment的問題(Execution Environment Ownership Problem)。
   subprocess會啟動current virtual environment

   - Solution:
   1. 使用current virtual environment
   2. 使用docker containerization 搭配 github action (進階)

   cmd
   ```python
   pytest	❌ 依賴 PATH
   python -m pytest	✅ 依賴 current interpreter
   ```
