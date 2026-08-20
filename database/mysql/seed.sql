USE fatiguesense;

INSERT INTO analysis
(
    session_id,
    user_id,
    image_filename,
    fatigue_score,
    risk_level,
    recommendation,
    evidence
)
VALUES
(
    'test-session-001',
    'user-001',
    'image_1_rested.jpg',
    20.5,
    'low',
    'Fatigue appears low. Maintain healthy sleep habits.',
    '["Low fatigue indicators detected."]'
);


INSERT INTO analysis
(
    session_id,
    user_id,
    image_filename,
    fatigue_score,
    risk_level,
    recommendation,
    evidence
)
VALUES
(
    'test-session-002',
    'user-001',
    'image_2_mild_fatigue.png',
    55.0,
    'moderate',
    'Take a short break and get adequate rest.',
    '["Moderate fatigue indicators detected."]'
);


INSERT INTO analysis
(
    session_id,
    user_id,
    image_filename,
    fatigue_score,
    risk_level,
    recommendation,
    evidence
)
VALUES
(
    'test-session-003',
    'user-001',
    'image_3_high_fatigue.webp',
    85.0,
    'high',
    'Take an immediate rest break and avoid activities requiring prolonged attention.',
    '["High fatigue indicators detected."]'
);