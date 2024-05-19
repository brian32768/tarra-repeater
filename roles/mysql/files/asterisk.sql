CREATE TABLE IF NOT EXISTS queue_members (
    queue_name VARCHAR(80) NOT NULL,
    interface VARCHAR(80) NOT NULL, -- e.g. SIP/123
    uniqueid VARCHAR(80) NOT NULL,
    membername VARCHAR(80),         -- e.g. Brian
    state_interface VARCHAR(80),
    penalty INTEGER DEFAULT 1,
    paused INTEGER DEFAULT 0, -- Asterisk 13.8.0 throws an error unless its INT
    ringinuse INTEGER, -- Vastra addition
    PRIMARY KEY(queue_name, interface)
);

-- This has been stripped down
CREATE TABLE IF NOT EXISTS sippeers (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    ipaddr VARCHAR(45),	      -- updated by Asterisk
    port INTEGER,	      -- updated by Asterisk
    regseconds INTEGER,       -- updated by Asterisk
    defaultuser VARCHAR(40), 
    fullcontact VARCHAR(80),  -- REQUIRED by asterisk
    regserver VARCHAR(20),    -- updated by Asterisk
    useragent VARCHAR(255),   -- updated by Asterisk
    lastms INTEGER, 	      -- updated by Asterisk
    host VARCHAR(40) DEFAULT 'dynamic', 
    type ENUM('friend','user','peer') DEFAULT 'friend', 
    context VARCHAR(40), -- 'local' | 'roaming'
    permit VARCHAR(95), 
    deny VARCHAR(95), 
    secret VARCHAR(40), 
--  md5secret VARCHAR(40), 
--  remotesecret VARCHAR(40), 
    transport ENUM('udp','tcp','tls','ws','wss','udp,tcp','tcp,udp') DEFAULT 'udp',
    dtmfmode ENUM('rfc2833','info','shortinfo','inband','auto') DEFAULT 'rfc2833', 
    directmedia ENUM('yes','no','nonat','update','outgoing') DEFAULT 'no', 
    nat VARCHAR(29) DEFAULT 'no', -- 'rport,comedia' for roaming phones
    callgroup VARCHAR(40) DEFAULT '1', 
    pickupgroup VARCHAR(40) DEFAULT '1', 
--  language VARCHAR(40), 
    disallow VARCHAR(200) DEFAULT 'all', 
    allow VARCHAR(200) DEFAULT 'ulaw|h263|h264',
    insecure VARCHAR(40),
--  trustrpid ENUM('yes','no'), 
--  progressinband ENUM('yes','no','never'), 
--  promiscredir ENUM('yes','no'), 
--  useclientcode ENUM('yes','no'), 
--  accountcode VARCHAR(40), 
--  setvar VARCHAR(200), 
--  amaflags VARCHAR(40), 
--  callcounter ENUM('yes','no'), 
--  busylevel INTEGER, 
--  allowoverlap ENUM('yes','no'), 
--  allowsubscribe ENUM('yes','no'), 
--  maxcallbitrate INTEGER, 
--  rfc2833compensate ENUM('yes','no'), 
    mailbox VARCHAR(40),     
--  `session-timers` ENUM('accept','refuse','originate'), 
--  `session-expires` INTEGER, 
--  `session-minse` INTEGER, 
--  `session-refresher` ENUM('uac','uas'), 
--  t38pt_usertpsource VARCHAR(40), 
    regexten VARCHAR(40), 
--  fromdomain VARCHAR(40), 
--  fromuser VARCHAR(40), 
    qualify VARCHAR(10) DEFAULT 'yes', -- Set 'no' for roaming phones or a number>2000 for slow phones
--  defaultip VARCHAR(45),
--  rtptimeout INTEGER, 
--  rtpholdtimeout INTEGER, 
--  sendrpid ENUM('yes','no'), 
--  outboundproxy VARCHAR(40), 
    callbackextension VARCHAR(40), 	 -- REQUIRED by asterisk
--  timert1 INTEGER, 
--  timerb INTEGER, 
    qualifyfreq INTEGER DEFAULT 60,  -- Probe phones every 60 seconds
--  constantssrc ENUM('yes','no'), 
--  contactpermit VARCHAR(95), 
--  contactdeny VARCHAR(95), 
--  usereqphone ENUM('yes','no'), 
--  textsupport ENUM('yes','no'), 
--  faxdetect ENUM('yes','no'), 
--  buggymwi ENUM('yes','no'), 
--  auth VARCHAR(40), 
    fullname VARCHAR(40), 
--  trunkname VARCHAR(40), 
    cid_number VARCHAR(40), 
--  callingpres ENUM('allowed_not_screened','allowed_passed_screen','allowed_failed_screen','allowed','prohib_not_screened','prohib_passed_screen','prohib_failed_screen','prohib'), 
--  mohinterpret VARCHAR(40), 
--  mohsuggest VARCHAR(40), 
--  parkinglot VARCHAR(40), 
    hasvoicemail ENUM('yes','no'), -- Asterisk should set this automatically
    subscribemwi ENUM('yes','no') DEFAULT 'yes',
--  vmexten VARCHAR(40), 
--  autoframing ENUM('yes','no'), 
--  rtpkeepalive INTEGER, 
    `call-limit` INTEGER DEFAULT 4, 
--  g726nonstandard ENUM('yes','no'), 
--  ignoresdpversion ENUM('yes','no'), 
    allowtransfer ENUM('yes','no') DEFAULT 'yes', 
    dynamic ENUM('yes','no') DEFAULT 'yes', 
--  path VARCHAR(256), 
--  supportpath ENUM('yes','no'), 

    # Might these be dead and removed???
    subscribecontext VARCHAR(80) DEFAULT 'phones',
    videosupport ENUM('yes','no') DEFAULT 'no', 
    callerid VARCHAR(40),

    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE INDEX sippeers_name ON sippeers (name);

CREATE INDEX sippeers_name_host ON sippeers (name, host);

CREATE INDEX sippeers_ipaddr_port ON sippeers (ipaddr, port);

CREATE INDEX sippeers_host_port ON sippeers (host, port);

-- This has been stripped down
CREATE TABLE IF NOT EXISTS voicemail (
    uniqueid INTEGER NOT NULL AUTO_INCREMENT, -- don't rename this
    context VARCHAR(80) NOT NULL DEFAULT 'default', 
    mailbox VARCHAR(80) NOT NULL,  -- DTMF number
    password VARCHAR(80) NOT NULL, -- DTMF number
    fullname VARCHAR(80), 
    alias VARCHAR(80), 
    email VARCHAR(80), 
    pager VARCHAR(80), 
    attach ENUM('yes','no') DEFAULT 'yes', 
    attachfmt VARCHAR(10) DEFAULT 'wav', 
    serveremail VARCHAR(80) DEFAULT 'localhost', 
    language VARCHAR(20), 
    tz VARCHAR(30), 
    deletevoicemail ENUM('yes','no') DEFAULT 'no', 
    heardvoicemail ENUM('yes','no') DEFAULT 'no', -- Vastra addition for Ledson
    saycid ENUM('yes','no'), 
    sendvoicemail ENUM('yes','no') DEFAULT 'no', 
    review ENUM('yes','no') DEFAULT 'no', 
    tempgreetwarn ENUM('yes','no') DEFAULT 'yes', 
    operator ENUM('yes','no') DEFAULT 'yes', 
    envelope ENUM('yes','no') DEFAULT 'no', 
    sayduration INTEGER DEFAULT 1, 
    forcename ENUM('yes','no'), 
    forcegreetings ENUM('yes','no'), 
    callback VARCHAR(80), 
    dialout VARCHAR(80), 
    exitcontext VARCHAR(80), 
    maxmsg INTEGER DEFAULT 1000, 
    volgain NUMERIC(5, 2), 
    imapuser VARCHAR(80), 
    imappassword VARCHAR(80),
    imapserver VARCHAR(80) DEFAULT 'localhost', 
    imapport VARCHAR(8) DEFAULT '993', 
    imapflags VARCHAR(80) DEFAULT 'ssl/novalidate-cert', 
    stamp DATETIME,
    PRIMARY KEY (uniqueid)
);

CREATE INDEX voicemail_mailbox ON voicemail (mailbox);

CREATE INDEX voicemail_context ON voicemail (context);

CREATE INDEX voicemail_mailbox_context ON voicemail (mailbox, context);

CREATE INDEX voicemail_imapuser ON voicemail (imapuser);

-- Vastra addition
CREATE TABLE IF NOT EXISTS holiday (
    date DATE NOT NULL PRIMARY KEY,   -- YYYY-MM-DD or %-MM-DD
    name VARCHAR(50)                  -- Christmas for example
);

INSERT INTO holiday (date,name) VALUES
('2016-07-04', 'Fourth of July'),
('2016-12-25', 'Christmas'),
('2017-01-01', 'New Years Day');

INSERT INTO holiday (date,name) VALUES ('2016-02-14', 'Valentines Day');
