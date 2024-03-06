CREATE TABLE IF NOT EXISTS overrides (
    member_dob DATE NOT NULL,
    member_id VARCHAR(50) NOT NULL,
    copay INT,
    coinsurance INT,
    deductible INT,
    oop_max INT,
    UNIQUE KEY unique_member_id_dob (member_id, member_dob)
);

SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Load data from CSV file into the table
LOAD DATA INFILE '/docker-entrypoint-initdb.d/overrides_sample.csv'
INTO TABLE overrides
FIELDS TERMINATED BY ',' -- Specify the field delimiter in your CSV file
ENCLOSED BY '"' -- Specify the field enclosure character in your CSV file
LINES TERMINATED BY '\n' -- Specify the line terminator in your CSV file
IGNORE 1 ROWS -- Skip the header row if it exists in the CSV file
(member_dob, member_id, @copay, @coinsurance, @deductible, @oop_max)
SET
  copay = NULLIF(@copay, ''),
  coinsurance = NULLIF(@coinsurance, ''),
  deductible = NULLIF(@deductible, ''),
  oop_max = NULLIF(@oop_max, '')
 ;