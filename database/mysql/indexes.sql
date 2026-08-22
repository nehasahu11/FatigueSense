USE fatiguesense;

CREATE INDEX idx_analysis_user
ON analysis(user_id);

CREATE INDEX idx_analysis_session
ON analysis(session_id);

CREATE INDEX idx_analysis_created
ON analysis(created_at);

CREATE INDEX idx_analysis_risk
ON analysis(risk_level);