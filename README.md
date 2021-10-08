# Ký hiệu được sử dụng để mô phỏng cho các đối tượng trong trò chơi sokoban:

- A : đại diện cho đối tượng mà người dùng điều khiển
- E : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: người dùng điều khiển và vị trí đích
- X : đại diện cho đối tượng các khối hộp cần được đẩy đến vị trí đích
- \# : đại diện cho đối tượng là các khối đá chắn(hoặc bức tường)
- \_ : đại diện cho đối tượng là vị trí đích mà ta cần đẩy khối hộp đến
- O : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: khối hộp và vị trí đích

# Hướng dẫn chạy code:

- Bước 1: nhập lệnh: pip install numpy time heapq
- Bước 2: nhập lệnh: python main.py
- Bước 3: lựa chọn input đầu vào (mini, micro) và kiểu giải thuật (DFS, Astar) cho bài toán

# Các input(trạng thái đầu game) nằm ở các file trong thư mục test/

# Các output(kết quả và hướng dẫn giải tường bước cho bài toán) nằm ở các file trong thư mục solutions/

# Thời gian chạy giải thuật được in ra tại màn hình console sau khi chạy hoàn tất, nếu giải thuật không tìm kiếm được kết quả khả thi màn hình console sẽ trả về thông báo "Can't find the solution"
