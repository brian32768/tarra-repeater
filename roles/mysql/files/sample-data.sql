INSERT INTO sippeers (`context`,`type`,`name`,`fullname`,`regexten`,`mailbox`,`defaultuser`,`secret`,`videosupport`,`callerid`,`cid_number`) VALUES ('internal-calls','friend','galaxy','BW (mobile)','103', '103@default', '103', 'aa12345',       'yes', 'Brian Wilson','707-827-0001');

INSERT INTO sippeers (`context`,`type`,`name`,`fullname`,`regexten`,`mailbox`,`defaultuser`,`secret`,`videosupport`,`callerid`,`cid_number`) VALUES ('internal-calls','friend','gxv3240','BHW','511', '511@default', '511', 'aa12345',       'yes', 'Brian Wilson','511');

INSERT INTO sippeers (`context`,`type`,`name`,`fullname`,`regexten`,`mailbox`,`defaultuser`,`secret`,`videosupport`,`callerid`,`cid_number`) VALUES ('internal-calls','friend','bt100','BHW','101', '101@default', '101', 'aa12345',       'no', 'Brian Wilson','100');

INSERT INTO `voicemail` (`context`, `mailbox`, `password`, `email`, `fullname`, `imapuser`, `imappassword`) VALUES
('default', '103', '0255', 'brian@wildsong.biz', 'Brian W', 'bwilson', 'buzzword');

