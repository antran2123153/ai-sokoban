## Ký hiệu được sử dụng để mô phỏng cho các đối tượng trong trò chơi sokoban:

- A : đại diện cho đối tượng mà người dùng điều khiển
- E : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: người dùng điều khiển và vị trí đích
- X : đại diện cho đối tượng các khối hộp cần được đẩy đến vị trí đích
- \# : đại diện cho đối tượng là các khối đá chắn(hoặc bức tường)
- \_ : đại diện cho đối tượng là vị trí đích mà ta cần đẩy khối hộp đến
- O : đại diện cho đối tượng mà tại đó có cả 2 đối tượng: khối hộp và vị trí đích

## Hướng dẫn chạy code:

- Bước 1: nhập lệnh:
  > pip install numpy
- Bước 2: nhập lệnh:
  > python main.py
- Bước 3: lựa chọn input đầu vào (mini, micro) và kiểu giải thuật (DFS, Astar) cho bài toán

## Thông tin thêm

- Thư mục inputs: chứa các trạng thái khởi đầu cho game, bao gồm 2 loại là mini và micro

- Thư mục output: là két quả giải từng bước của input đầu vào tương ứng sau khi chạy giải thuật

- Thời gian chạy giải thuật được in ra tại màn hình console sau khi chạy hoàn tất, nếu giải thuật không tìm kiếm được kết quả khả thi màn hình console sẽ trả về thông báo "Can't find the solution" nếu có sẽ trả về số bước đi mà giải thuật tìm kiếm được và in ra file output

## Ví dụ cho kết quả của màn hình console sau khi chạy xong:

```
Select input type (1 - Mini Comos, 2 - Micro Comos): 1
Select lever (1 - 60): 20
Select search algorithm (1 - DFS algorithm, 2 - A start algorithm): 2
Using the A start algorithm to solve...
Runtime: 2.8360002040863037 second.
Total step: 113
```
