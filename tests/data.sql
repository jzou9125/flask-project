
INSERT INTO user (username, email, password)
VALUES
  ('test', 'a@a', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 's@s', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');
  -- ('test', 'a@a', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),


INSERT INTO admin (username, email, password)
VALUES ("admin", "admin@a", 'pbkdf2:sha256:260000$fUwdu0GWL2SOBKYE$41fd8aacde82420a61a67dac5ce1c21e902d9f62ba5bec2ec6ff0e94cb0dad56')