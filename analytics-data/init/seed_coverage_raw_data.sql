CREATE TABLE IF NOT EXISTS coverage_raw (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    member_id VARCHAR(50),
    member_dob DATE,
    payer_id VARCHAR(50),
    response_copay INT,
    response_coinsurance INT,
    response_deductible INT,
    response_oop_max INT,
    ch_response_copay INT,
    ch_response_coinsurance INT,
    ch_response_deductible INT,
    ch_response_oop_max INT,
    overriden BOOL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_member (member_id, member_dob, timestamp)
);

SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

LOAD DATA INFILE '/docker-entrypoint-initdb.d/coverage_raw.csv'
INTO TABLE coverage_raw
FIELDS TERMINATED BY ',' -- Specify the field delimiter in your CSV file
ENCLOSED BY '"' -- Specify the field enclosure character in your CSV file
LINES TERMINATED BY '\n' -- Specify the line terminator in your CSV file
IGNORE 1 ROWS -- Skip the header row if it exists in the CSV file
(customer_id, member_id, member_dob, payer_id, @response_copay, @response_coinsurance, @response_deductible, @response_oop_max, @ch_response_copay, @ch_response_coinsurance, @ch_response_deductible, @ch_response_oop_max, overriden, @timestamp)
SET
  response_copay = NULLIF(@response_copay, ''),
  response_coinsurance = NULLIF(@response_coinsurance, ''),
  response_deductible = NULLIF(@response_deductible, ''),
  response_oop_max = NULLIF(@response_oop_max, ''),
  ch_response_copay = NULLIF(@ch_response_copay, ''),
  ch_response_coinsurance = NULLIF(@ch_response_coinsurance, ''),
  ch_response_deductible = NULLIF(@ch_response_deductible, ''),
  ch_response_oop_max = NULLIF(@ch_response_oop_max, ''),
  timestamp = STR_TO_DATE(@timestamp, '%c/%e/%Y') 
;


CREATE TABLE IF NOT EXISTS api_calls (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    member_id VARCHAR(50),
    member_dob DATE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_member (member_id, member_dob, timestamp)
);

CREATE TABLE IF NOT EXISTS members (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    member_id VARCHAR(50),
    member_dob DATE,
    payer_id VARCHAR(50),
    overriden_times INT,
    UNIQUE KEY unique_member (member_id, member_dob)
);