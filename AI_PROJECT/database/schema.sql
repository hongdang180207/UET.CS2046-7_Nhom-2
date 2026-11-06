--1.TẠO DATABASE
CREATE DATABASE IF NOT EXISTS chi_tieu_sinh_vien
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
--Chọn database
USE chi_tieu_sinh_vien;

--2.NGƯỜI DÙNG
CREATE TABLE IF NOT EXISTS users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

--3.DANH MỤC THU CHI
CREATE TABLE IF NOT EXISTS categories (
    category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    -- Không cho tạo trùng tên danh mục trong cùng loại thu hoặc chi
    UNIQUE KEY uq_categories_name_type (name, type)
) ENGINE=InnoDB;

-- 4. Giao dịch thu chi
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    transaction_type ENUM('income', 'expense') NOT NULL,
    amount_vnd BIGINT UNSIGNED NOT NULL,
    description VARCHAR(500),
    transaction_date DATE NOT NULL,
    input_source ENUM('manual', 'natural_language')
        NOT NULL DEFAULT 'manual',
    exclude_from_saving BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transactions_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT,

    INDEX idx_transactions_user_date (user_id, transaction_date),
    INDEX idx_transactions_category (category_id)
) ENGINE=InnoDB;


-- 5. Thiết lập ngân sách của người dùng
CREATE TABLE IF NOT EXISTS budget_settings (
    setting_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    monthly_budget_vnd BIGINT UNSIGNED NOT NULL DEFAULT 0,
    payday TINYINT UNSIGNED,
    reserve_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.1000,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- Mỗi người dùng có một thiết lập ngân sách
    UNIQUE KEY uq_budget_settings_user (user_id),

    CONSTRAINT fk_budget_settings_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


-- 6. Các khoản chi bắt buộc, ví dụ tiền trọ hoặc học phí
CREATE TABLE IF NOT EXISTS required_expenses (
    expense_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    name VARCHAR(150) NOT NULL,
    amount_vnd BIGINT UNSIGNED NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('unpaid', 'paid', 'cancelled')
        NOT NULL DEFAULT 'unpaid',
    paid_transaction_id BIGINT UNSIGNED,

    CONSTRAINT fk_required_expenses_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    -- Có thể liên kết khoản bắt buộc đã trả với giao dịch thực tế
    CONSTRAINT fk_required_expenses_paid_transaction
        FOREIGN KEY (paid_transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE SET NULL,

    INDEX idx_required_expenses_user_due (user_id, due_date)
) ENGINE=InnoDB;


-- 7. Mục tiêu tiết kiệm
CREATE TABLE IF NOT EXISTS saving_goals (
    goal_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    name VARCHAR(150) NOT NULL,
    target_amount_vnd BIGINT UNSIGNED NOT NULL,
    deadline DATE NOT NULL,
    status ENUM('active', 'completed', 'paused', 'cancelled')
        NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_saving_goals_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    INDEX idx_saving_goals_user_status (user_id, status)
) ENGINE=InnoDB;


-- 8. Mức chi nền theo danh mục tại thời điểm đặt mục tiêu tiết kiệm
CREATE TABLE IF NOT EXISTS goal_baselines (
    baseline_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    goal_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    daily_baseline_vnd BIGINT UNSIGNED NOT NULL,

    -- Mỗi mục tiêu chỉ có một mức chi nền cho mỗi danh mục
    UNIQUE KEY uq_goal_baselines_goal_category (goal_id, category_id),

    CONSTRAINT fk_goal_baselines_goal
        FOREIGN KEY (goal_id) REFERENCES saving_goals(goal_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_goal_baselines_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;


-- 9. Thêm các danh mục ban đầu
INSERT IGNORE INTO categories (name, type) VALUES
    ('Ăn uống', 'expense'),
    ('Cà phê/trà sữa', 'expense'),
    ('Đi lại', 'expense'),
    ('Nhà trọ', 'expense'),
    ('Học tập', 'expense'),
    ('Giải trí', 'expense'),
    ('Mua sắm', 'expense'),
    ('Sức khỏe', 'expense'),
    ('Khác', 'expense'),
    ('Gia đình gửi', 'income'),
    ('Làm thêm', 'income'),
    ('Học bổng', 'income'),
    ('Khác', 'income');
