Run code:
Step 1: pip install numpy time heapq
Step 2: python main.py
Step 3: select options

See initial game state in folder test/
See solutions step-by-step in folder solutions/<file name initial game state>

Ký hiệu được sử dụng để mô phỏng cho các đối tượng trong trò chơi sokoban:
- A : đại diện cho đối tượng mà người dùng điều khiển
- E : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: người dùng điều khiển và vị trí đích
- X : đại diện cho đối tượng các khối hộp cần được đẩy đến vị trí đích
- # : đại diện cho đối tượng là các khối đá chắn(hoặc bức tường)
- _ : đại diện cho đối tượng là vị trí đích mà ta cần đẩy khối hộp đến
- O : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: khối hộp và vị trí đích

