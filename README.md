1. Tệp 'main.py': Chứa code để chạy ứng dụng, nó sẽ import gói controller và gọi hàm tạo ra cửa sổ chính.

2. Gói 'model': Chứa tất cả các mã liên quan đến mô hình dữ liệu của ứng dụng.
 - tệp '__init__.py': Tệp này trống và thư mục model chứa nó sẽ được python coi là một gói.
 - tệp 'image_processing.py': Chứa tất cả các mã liên quan đến xử lý hình ảnh và trích xuất văn bản bằng pytesseract.

3. Gói 'view': Chứa tất cả các mã liên quan đến giao diện người dùng của ứng dụng.
- tệp '__init__.py': Tệp này trống và thư mục model chứa nó sẽ được python coi là một gói.
- tệp 'main_window.py': Chứa các mã liên quan đến việc tạo và thiết lập cửa sổ chính của ứng dụng.

4. Gói 'controller': Chứa tất cả các mã liên quan đến việc xử lý tương tác của người dùng và cập nhật mô hình và xem cho phù hợp.
- tệp '__init__.py': Tệp này trống và thư mục model chứa nó sẽ được python coi là một gói.
- tệp 'text_extractor.py': Chứa mã kết nối mô hình và view với nhau và xử lý tương tác của người dùng

5. Thư mục: 'resources': Chứa tất cả các tài nguyên như các biểu tượng được ứng dụng sử dụng, các hình ảnh dùng để trích xuất văn bản.
- thư mục: 'icon': Chứa các biểu tượng được ứng dụng sử dụng như tải lên, trích xuất và sao chép các biểu tượng.
- thư mục: 'images': Chứa các hình ảnh dùng để trích xuất văn bản