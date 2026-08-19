USE fatiguesense;

CREATE TABLE IF NOT EXISTS analysis (

    id INT AUTO_INCREMENT PRIMARY KEY,

    session_id VARCHAR(100)
        NOT NULL UNIQUE,

    user_id VARCHAR(100),

    image_filename VARCHAR(255),

    fatigue_score FLOAT NOT NULL,

    risk_level VARCHAR(50) NOT NULL,

    recommendation TEXT,

    evidence TEXT,

    created_at DATETIME
        DEFAULT CURRENT_TIMESTAMP

);