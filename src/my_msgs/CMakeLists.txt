cmake_minimum_required(VERSION 3.8)   # CMakeの最低バージョン指定(3.8以上でビルド)
project(my_msgs)                      # プロジェクト名定義

# コンパイラ設定
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ament(ROS2ビルドシステム)読込み
find_package(ament_cmake REQUIRED)

# msg/srv/action のコード生成するパッケージ
find_package(rosidl_default_generators REQUIRED)

# msgファイルをビルド対象に登録
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RoombaController.msg"
)

# テスト関連
if(BUILD_TESTING)
  # コードの静的チェックツール
  find_package(ament_lint_auto REQUIRED)
  # 著作権情報をチェックするリンターをスキップ
  # すべてのソースファイルに著作権及びライセンス情報が追加されたらコメントアウト
  set(ament_cmake_copyright_FOUND TRUE)
  # cpplint をスキップ（Gitリポジトリ内でのみ有効）
  # このパッケージが Git リポジトリ内にある場合、および
  # すべてのソースファイルに著作権表示とライセンスが追加されたらコメントアウト
  set(ament_cmake_cpplint_FOUND TRUE)
  # テスト用の依存関係を自動検出
  ament_lint_auto_find_test_dependencies()
endif()

# このパッケージをROS2パッケージとして確定させる
ament_package()
