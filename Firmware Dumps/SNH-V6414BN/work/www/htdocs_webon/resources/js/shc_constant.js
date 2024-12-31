var TIME_ZONE_LIST = new Array(97);
	TIME_ZONE_LIST[0] = new Array('(GMT-12:00) International Date Line West',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[1] = new Array('(GMT-11:00) Samoa',												9,			5,0,0,0,0,4,1,0,0,0,0);
	TIME_ZONE_LIST[2] = new Array('(GMT-11:00) Coordinated Universal Time-11',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[3] = new Array('(GMT-10:00) Hawaii',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[4] = new Array('(GMT-09:00) Alaska',												3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[5] = new Array('(GMT-08:00) Pacific Time (US & Canada)',							3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[6] = new Array('(GMT-08:00) Baja California',									4,			1,0,2,0,0,10,5,0,2,0,0);
	TIME_ZONE_LIST[7] = new Array('(GMT-07:00) Chihuahua, La Paz, Mazatlan',						4,			1,0,2,0,0,10,5,0,2,0,0);
	TIME_ZONE_LIST[8] = new Array('(GMT-07:00) Mountain Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[9] = new Array('(GMT-07:00) Arizona',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[10] = new Array('(GMT-06:00) Saskatchewan',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[11] = new Array('(GMT-06:00) Central America',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[12] = new Array('(GMT-06:00) Central Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[13] = new Array('(GMT-06:00) Guadalajara, Mexico City, Monterrey',				4,			1,0,2,0,0,10,5,0,2,0,0);
	TIME_ZONE_LIST[14] = new Array('(GMT-05:00) Eastern Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[15] = new Array('(GMT-05:00) Bogota, Lima, Quito',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[16] = new Array('(GMT-05:00) Indiana (East)',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[17] = new Array('(GMT-04:30) Caracas',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[18] = new Array('(GMT-04:00) Atlantic Time (Canada)',							3,			2,0,2,0,0,11,1,0,2,0,0);
	TIME_ZONE_LIST[19] = new Array('(GMT-04:00) Cuiaba',											10,			3,0,0,0,0,2,3,0,0,0,0);
	TIME_ZONE_LIST[20] = new Array('(GMT-04:00) Santiago',											10,			2,0,0,0,0,3,2,0,0,0,0);
	TIME_ZONE_LIST[21] = new Array('(GMT-04:00) Asuncion',											10,			3,0,0,0,0,3,2,0,0,0,0);
	TIME_ZONE_LIST[22] = new Array('(GMT-04:00) Georgetown, La Paz, Manaus, San Juan',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[23] = new Array('(GMT-03:30) Newfoundland',										3,			2,0,0,1,0,11,1,0,0,1,0);
	TIME_ZONE_LIST[24] = new Array('(GMT-03:00) Buenos Aires',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[25] = new Array('(GMT-03:00) Brasilia',											10,			3,0,0,0,0,2,3,0,0,0,0);
	TIME_ZONE_LIST[26] = new Array('(GMT-03:00) Greenland',											3,			5,6,22,0,0,10,5,6,23,0,0);
	TIME_ZONE_LIST[27] = new Array('(GMT-03:00) Montevideo',										10,			1,0,2,0,0,3,2,0,2,0,0);
	TIME_ZONE_LIST[28] = new Array('(GMT-03:00) Cayenne, Fortaleza',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[29] = new Array('(GMT-02:00) Mid-Atlantic',										3,			5,0,2,0,0,9,5,0,2,0,0);
	TIME_ZONE_LIST[30] = new Array('(GMT-02:00) Coordinated Universal Time-02',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[31] = new Array('(GMT-01:00) Azores',											3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[32] = new Array('(GMT-01:00) Cape Verde Is.',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[33] = new Array('(GMT) Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London',	3,			5,0,1,0,0,10,5,0,2,0,0);
	TIME_ZONE_LIST[34] = new Array('(GMT) Monrovia, Reykjavik',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[35] = new Array('(GMT) Casablanca',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[36] = new Array('(GMT) Coordinated Universal Time',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[37] = new Array('(GMT+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague',	3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[38] = new Array('(GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb',					3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[39] = new Array('(GMT+01:00) Brussels, Copenhagen, Madrid, Paris',				3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[40] = new Array('(GMT+01:00) West Central Africa',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[41] = new Array('(GMT+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna',	3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[42] = new Array('(GMT+02:00) Minsk',												3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[43] = new Array('(GMT+02:00) Cairo',												4,			5,5,0,0,0,9,5,4,23,59,59);
	TIME_ZONE_LIST[44] = new Array('(GMT+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius',		3,			5,0,3,0,0,10,5,0,4,0,0);
	TIME_ZONE_LIST[45] = new Array('(GMT+02:00) Athens, Bucharest, Istanbul',						3,			5,0,3,0,0,10,5,0,4,0,0);
	TIME_ZONE_LIST[46] = new Array('(GMT+02:00) Jerusalem',											3,			5,5,2,0,0,9,2,0,2,0,0);
	TIME_ZONE_LIST[47] = new Array('(GMT+02:00) Amman',												3,			5,4,23,59,59,10,5,5,1,0,0);
	TIME_ZONE_LIST[48] = new Array('(GMT+02:00) Beirut',											3,			5,0,0,0,0,10,5,0,0,0,0);
	TIME_ZONE_LIST[49] = new Array('(GMT+02:00) Windhoek',											4,			1,0,2,0,0,9,1,0,2,0,0);
	TIME_ZONE_LIST[50] = new Array('(GMT+02:00) Harare, Pretoria',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[51] = new Array('(GMT+03:00) Kuwait, Riyadh',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[52] = new Array('(GMT+03:00) Baghdad',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[53] = new Array('(GMT+03:00) Nairobi',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[54] = new Array('(GMT+03:00) Moscow, St. Petersburg, Volgograd',					3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[55] = new Array('(GMT+03:30) Tehran',											3,			3,0,0,0,0,9,3,2,0,0,0);
	TIME_ZONE_LIST[56] = new Array('(GMT+04:00) Abu Dhabi, Muscat',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[57] = new Array('(GMT+04:00) Yerevan',											3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[58] = new Array('(GMT+04:00) Baku',												3,			5,0,4,0,0,10,5,0,5,0,0);
	TIME_ZONE_LIST[59] = new Array('(GMT+04:00) Caucasus Standard Time',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[60] = new Array('(GMT+04:00) Tbilisi',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[61] = new Array('(GMT+04:00) Port Louis',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[62] = new Array('(GMT+04:30) Kabul',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[63] = new Array('(GMT+05:00) Ekaterinburg',										3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[64] = new Array('(GMT+05:00) Islamabad, Karachi',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[65] = new Array('(GMT+05:00) Tashkent',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[66] = new Array('(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[67] = new Array('(GMT+05:30) Sri Jayawardenepura',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[68] = new Array('(GMT+05:45) Kathmandu',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[69] = new Array('(GMT+06:00) Dhaka',												3,			5,3,22,59,0,10,5,0,23,59,0);
	TIME_ZONE_LIST[70] = new Array('(GMT+06:00) Astana',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[71] = new Array('(GMT+06:00) Novosibirsk',										3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[72] = new Array('(GMT+06:30) Yangon (Rangoon)',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[73] = new Array('(GMT+07:00) Krasnoyarsk',										3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[74] = new Array('(GMT+07:00) Bangkok, Hanoi, Jakarta',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[75] = new Array('(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[76] = new Array('(GMT+08:00) Irkutsk',											3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[77] = new Array('(GMT+08:00) Kuala Lumpur, Singapore',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[78] = new Array('(GMT+08:00) Taipei',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[79] = new Array('(GMT+08:00) Ulaanbaatar',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[80] = new Array('(GMT+08:00) Perth',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[81] = new Array('(GMT+09:00) Seoul',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[82] = new Array('(GMT+09:00) Osaka, Sapporo, Tokyo',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[83] = new Array('(GMT+09:00) Yakutsk',											3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[84] = new Array('(GMT+09:30) Darwin',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[85] = new Array('(GMT+09:30) Adelaide',											10,			1,0,2,0,0,4,1,0,3,0,0);
	TIME_ZONE_LIST[86] = new Array('(GMT+10:00) Canberra, Melbourne, Sydney',						10,			1,0,2,0,0,4,1,0,3,0,0);
	TIME_ZONE_LIST[87] = new Array('(GMT+10:00) Brisbane',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[88] = new Array('(GMT+10:00) Hobart',											10,			1,0,2,0,0,4,1,0,3,0,0);
	TIME_ZONE_LIST[89] = new Array('(GMT+10:00) Vladivostok',										3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[90] = new Array('(GMT+10:00) Guam, Port Moresby',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[91] = new Array('(GMT+11:00) Magadan, Solomon Is., New Caledonia',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[92] = new Array('(GMT+12:00) Fiji',												11,			5,0,2,0,0,4,5,0,3,0,0);
	TIME_ZONE_LIST[93] = new Array('(GMT+12:00) Petropavlovsk-Kamchatsky',							3,			5,0,2,0,0,10,5,0,3,0,0);
	TIME_ZONE_LIST[94] = new Array('(GMT+12:00) Auckland, Wellington',								9,			5,0,2,0,0,4,1,0,3,0,0);
	TIME_ZONE_LIST[95] = new Array('(GMT+12:00) Coordinated Universal Time+12',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
	TIME_ZONE_LIST[96] = new Array("(GMT+13:00) Nuku'alofa",										'invalid',	0,0,0,0,0,0,0,0,0,0,0);

var TIME_ZONE_NAME = new Array(
	"STWT12",									// (GMT-12:00) 날짜 변경선 서쪽
	"STWT11STWST,M9.5.0/0,M4.1.0/0", 			// (GMT-11:00) 사모아
	"STWT11",									// (GMT-11:00) 협정 세계시-11
	"STWT10",									// (GMT-10:00) 하와이
	"STWT9STWST,M3.2.0,M11.1.0",				// (GMT-09:00) 알래스카
	"STWT8STWST,M3.2.0,M11.1.0",				// (GMT-08:00) 태평양 표준시 (미국과 캐나다)
	"STWT8STWST,M4.1.0,M10.5.0",				// (GMT-08:00) 바하 캘리포니아
	"STWT7STWST,M4.1.0,M10.5.0",				// (GMT-07:00) 치와와, 라파스, 마사틀란
	"STWT7STWST,M3.2.0,M11.1.0",				// (GMT-07:00) 산지 표준시 (미국과 캐나다)
	"STWT7",									// (GMT-07:00) 애리조나
	"STWT6",									// (GMT-06:00) 서스캐처원
	"STWT6",									// (GMT-06:00) 중앙 아메리카
	"STWT6STWST,M3.2.0,M11.1.0",				// (GMT-06:00) 중부 표준시 (미국과 캐나다)
	"STWT6STWST,M4.1.0,M10.5.0",				// (GMT-06:00) 과달라하라, 멕시코시티, 몬테레이
	"STWT5STWST,M3.2.0,M11.1.0",				// (GMT-05:00) 동부 표준시 (미국과 캐나다)
	"STWT5",									// (GMT-05:00) 보고타, 리마, 키토
	"STWT5",									// (GMT-05:00) 인디애나 (동부)
	"STWT4:30", 								// (GMT-04:30) 카라카스
	"STWT4STWST,M3.2.0,M11.1.0",				// (GMT-04:00) 대서양 표준시 (캐나다)
	"STWT4STWST,M10.3.0/0,M2.3.0/0",			// (GMT-04:00) 쿠이아바
	"STWT4STWST,M10.2.0/0,M3.2.0/0",			// (GMT-04:00) 산티아고
	"STWT4STWST,M10.3.0/0,M3.2.0/0",			// (GMT-04:00) 아순시온
	"STWT4",									// (GMT-04:00) 조지타운, 라파스, 마노스, 산후안
	"STWT3:30STWST,M3.2.0/0:1,M11.1.0/0:1", 	// (GMT-03:30) 뉴펀들랜드
	"STWT3",									// (GMT-03:00) 부에노스아이레스
	"STWT3STWST,M10.3.0/0,M2.3.0/0",			// (GMT-03:00) 브라질리아
	"STWT3STWST,M3.5.6/22,M10.5.6/23",			// (GMT-03:00) 그린랜드
	"STWT3STWST,M10.1.0,M3.2.0",				// (GMT-03:00) 몬테비디오
	"STWT3",									// (GMT-03:00) 카옌, 포르탈레자
	"STWT2STWST,M3.5.0,M9.5.0", 				// (GMT-02:00) 중부-대서양
	"STWT2",									// (GMT-02:00) 협정 세계시-02
	"STWT1STWST,M3.5.0,M10.5.0/3",				// (GMT-01:00) 아조레스
	"STWT1",									// (GMT-01:00) 까뽀베르데 군도
	"STWT0STWST,M3.5.0/1,M10.5.0",				// (GMT) 그리니치 표준시; 더블린, 에딘버러, 리스본, 런던
	"STWT0",									// (GMT) 몬로비아, 레이캬비크
	"STWT0",									// (GMT) 카사블랑카
	"STWT0",									// (GMT) 협정 세계시
	"STWT-1STWST,M3.5.0,M10.5.0/3", 			// (GMT+01:00) 베오그라드, 브라티슬라바, 부다페스트, 루블랴나, 프라하
	"STWT-1STWST,M3.5.0,M10.5.0/3", 			// (GMT+01:00) 사라예보, 스코페, 바르샤바, 자그레브
	"STWT-1STWST,M3.5.0,M10.5.0/3", 			// (GMT+01:00) 브뤼셀, 코펜하겐, 마드리드, 파리
	"STWT-1",									// (GMT+01:00) 서중앙 아프리카
	"STWT-1STWST,M3.5.0,M10.5.0/3", 			// (GMT+01:00) 암스테르담, 베를린, 베른, 로마, 스톡홀름, 빈
	"STWT-2STWST,M3.5.0,M10.5.0/3", 			// (GMT+02:00) 민스크
	"STWT-2STWST,M4.5.5/0,M9.5.4/23:59:59",		// (GMT+02:00) 카이로
	"STWT-2STWST,M3.5.0/3,M10.5.0/4",			// (GMT+02:00) 헬싱키, 키예프, 리가, 소피아, 탈린, 빌뉴스
	"STWT-2STWST,M3.5.0/3,M10.5.0/4",			// (GMT+02:00) 아테네, 부카레스트, 이스탄불
	"STWT-2STWST,M3.5.5,M9.2.0",				// (GMT+02:00) 예루살렘
	"STWT-2STWST,M3.5.4/23:59:59,M10.5.5/1",	// (GMT+02:00) 암만
	"STWT-2STWST,M3.5.0/0,M10.5.0/0",			// (GMT+02:00) 베이루트
	"STWT-2STWST-3,M4.1.0,M9.1.0",				// (GMT+02:00) 빈트후크
	"STWT-2",									// (GMT+02:00) 하라레, 프리토리아
	"STWT-3",									// (GMT+03:00) 쿠웨이트, 리야드
	"STWT-3",									// (GMT+03:00) 바그다드
	"STWT-3",									// (GMT+03:00) 나이로비
	"STWT-3STWST,M3.5.0,M10.5.0/3", 			// (GMT+03:00) 모스크바, 상트페테르부르그, 볼고그라드
	"STWT-3:30STWST,M3.3.0/0,M9.3.2/0", 		// (GMT+03:30) 테헤란
	"STWT-4",									// (GMT+04:00) 아부다비, 무스카트
	"STWT-4STWST,M3.5.0,M10.5.0/3", 			// (GMT+04:00) 예레반
	"STWT-4STWST,M3.5.0/4,M10.5.0/5",			// (GMT+04:00) 바쿠
	"STWT-4",									// (GMT+04:00) 코코서스 표준시
	"STWT-4",									// (GMT+04:00) 트빌리시
	"STWT-4",									// (GMT+04:00) 포트루이스
	"STWT-4:30",								// (GMT+04:30) 카불
	"STWT-5STWST,M3.5.0,M10.5.0/3", 			// (GMT+05:00) 에카테린부르그
	"STWT-5",									// (GMT+05:00) 이슬라마바드, 카라치
	"STWT-5",									// (GMT+05:00) 타슈켄트
	"STWT-5:30",								// (GMT+05:30) 첸나이, 콜카타, 뭄바이, 뉴델리
	"STWT-5:30",								// (GMT+05:30) 스리자야와르데네푸라
	"STWT-5:45",								// (GMT+05:45) 카트만두
	"STWT-6STWST,M3.5.3/22:59,M10.5.0/23:59",	// (GMT+06:00) 다카
	"STWT-6",									// (GMT+06:00) 아스타나
	"STWT-6STWST,M3.5.0,M10.5.0/3", 			// (GMT+06:00) 노보시비르스크
	"STWT-6:30",								// (GMT+06:30) 양곤
	"STWT-7STWST,M3.5.0,M10.5.0/3", 			// (GMT+07:00) 크라스노야스크
	"STWT-7",									// (GMT+07:00) 방콕, 하노이, 자카르타
	"STWT-8",									// (GMT+08:00) 베이징, 충칭, 홍콩 특별 행정구, 우루무치
	"STWT-8STWST,M3.5.0,M10.5.0/3", 			// (GMT+08:00) 이르쿠츠크
	"STWT-8",									// (GMT+08:00) 쿠알라룸푸, 싱가포르
	"STWT-8",									// (GMT+08:00) 타이베이
	"STWT-8",									// (GMT+08:00) 울란바토르
	"STWT-8",									// (GMT+08:00) 퍼스
	"STWT-9",									// (GMT+09:00) 서울
	"STWT-9",									// (GMT+09:00) 오사카, 삿포로, 도쿄
	"STWT-9STWST,M3.5.0,M10.5.0/3", 			// (GMT+09:00) 야쿠츠크
	"STWT-9:30",								// (GMT+09:30) 다윈
	"STWT-9:30STWST,M10.1.0,M4.1.0/3",			// (GMT+09:30) 아델라이드
	"STWT-10STWST,M10.1.0,M4.1.0/3",			// (GMT+10:00) 캔버라, 멜버른, 시드니
	"STWT-10",									// (GMT+10:00) 브리즈번
	"STWT-10STWST,M10.1.0,M4.1.0/3",			// (GMT+10:00) 호바트
	"STWT-10STWST,M3.5.0,M10.5.0/3",			// (GMT+10:00) 블라디보스톡
	"STWT-10",									// (GMT+10:00) 괌, 포트모르즈비
	"STWT-11",									// (GMT+11:00) 마가단, 솔로몬 군도, 뉴 칼레도니아
	"STWT-12STWST,M11.5.0,M4.5.0/3",			// (GMT+12:00) 피지
	"STWT-12STWST,M3.5.0,M10.5.0/3",			// (GMT+12:00) 페트로파블로프스크-캄차스키
	"STWT-12STWST,M9.5.0,M4.1.0/3", 			// (GMT+12:00) 오클랜드, 웰링턴
	"STWT-12",									// (GMT+12:00) 협정 세계시+12
	"STWT-13",									// (GMT+13:00) 누쿠알로파
	""											// Custom (User-Defined) Timezone
);

var TIME_ZONE_LIST_V2 = new Array(100);
TIME_ZONE_LIST_V2[0] = new Array('(GMT-12:00) International Date Line West',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[1] = new Array('(GMT-11:00) Coordinated Universal Time-11',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[2] = new Array('(GMT-10:00) Hawaii',												'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[3] = new Array('(GMT-09:00) Alaska',												3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[4] = new Array('(GMT-08:00) Pacific Time (US & Canada)',							3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[5] = new Array('(GMT-08:00) Baja California',									4,			1,0,2,0,0,10,5,0,2,0,0);
TIME_ZONE_LIST_V2[6] = new Array('(GMT-07:00) Chihuahua, La Paz, Mazatlan',						4,			1,0,2,0,0,10,5,0,2,0,0);
TIME_ZONE_LIST_V2[7] = new Array('(GMT-07:00) Mountain Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[8] = new Array('(GMT-07:00) Arizona',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[9] = new Array('(GMT-06:00) Saskatchewan',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[10] = new Array('(GMT-06:00) Central America',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[11] = new Array('(GMT-06:00) Central Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[12] = new Array('(GMT-06:00) Guadalajara, Mexico City, Monterrey',				4,			1,0,2,0,0,10,5,0,2,0,0);
TIME_ZONE_LIST_V2[13] = new Array('(GMT-05:00) Eastern Time (US & Canada)',						3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[14] = new Array('(GMT-05:00) Bogota, Lima, Quito',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
//TIME_ZONE_LIST_V2[15] = new Array('(GMT-05:00) Indiana (East)',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[15] = new Array('(GMT-05:00) Indiana (East)',									3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[16] = new Array('(GMT-04:30) Caracas',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[17] = new Array('(GMT-04:00) Atlantic Time (Canada)',							3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[18] = new Array('(GMT-04:00) Cuiaba',											10,			3,6,23,59,59,2,3,6,23,59,59);
TIME_ZONE_LIST_V2[19] = new Array('(GMT-04:00) Santiago',											10,			2,6,23,59,59,3,2,6,23,59,59);
TIME_ZONE_LIST_V2[20] = new Array('(GMT-04:00) Asuncion',											10,			1,6,23,59,59,4,2,6,23,59,59);
TIME_ZONE_LIST_V2[21] = new Array('(GMT-04:00) Georgetown, La Paz, Manaus, San Juan',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[22] = new Array('(GMT-03:30) Newfoundland',										3,			2,0,2,0,0,11,1,0,2,0,0);
TIME_ZONE_LIST_V2[23] = new Array('(GMT-03:00) Buenos Aires',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[24] = new Array('(GMT-03:00) El Salvador',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[25] = new Array('(GMT-03:00) Brasilia',											10,			3,6,23,59,59,2,3,6,23,59,59);
TIME_ZONE_LIST_V2[26] = new Array('(GMT-03:00) Greenland',										3,			5,6,22,0,0,10,5,6,23,0,0);
TIME_ZONE_LIST_V2[27] = new Array('(GMT-03:00) Montevideo',										10,			1,0,2,0,0,3,2,0,2,0,0);
TIME_ZONE_LIST_V2[28] = new Array('(GMT-03:00) Cayenne, Fortaleza',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[29] = new Array('(GMT-02:00) Mid-Atlantic',										3,			5,0,2,0,0,9,5,0,2,0,0);
TIME_ZONE_LIST_V2[30] = new Array('(GMT-02:00) Coordinated Universal Time-02',					'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[31] = new Array('(GMT-01:00) Azores',											3,			5,6,23,59,59,10,5,0,1,0,0);
TIME_ZONE_LIST_V2[32] = new Array('(GMT-01:00) Cape Verde Is.',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[33] = new Array('(GMT) Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London',3,			5,0,1,0,0,10,5,0,2,0,0);
TIME_ZONE_LIST_V2[34] = new Array('(GMT) Monrovia, Reykjavik',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[35] = new Array('(GMT) Casablanca',												4,			5,0,2,0,0,9,5,0,3,0,0);
TIME_ZONE_LIST_V2[36] = new Array('(GMT) Coordinated Universal Time',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[37] = new Array('(GMT+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague',3,			5,0,2,0,0,10,5,0,3,0,0);
TIME_ZONE_LIST_V2[38] = new Array('(GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb',					3,			5,0,2,0,0,10,5,0,3,0,0);
TIME_ZONE_LIST_V2[39] = new Array('(GMT+01:00) Windhoek',											9,			1,0,2,0,0,4,1,0,2,0,0);
TIME_ZONE_LIST_V2[40] = new Array('(GMT+01:00) Brussels, Copenhagen, Madrid, Paris',				3,			5,0,2,0,0,10,5,0,3,0,0);
TIME_ZONE_LIST_V2[41] = new Array('(GMT+01:00) West Central Africa',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[42] = new Array('(GMT+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna',	3,			5,0,2,0,0,10,5,0,3,0,0);
TIME_ZONE_LIST_V2[43] = new Array('(GMT+02:00) East Europe',										3,			5,0,2,0,0,10,5,0,3,0,0);
TIME_ZONE_LIST_V2[44] = new Array('(GMT+02:00) Cairo',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[45] = new Array('(GMT+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius',	3,			5,0,3,0,0,10,5,0,4,0,0);
TIME_ZONE_LIST_V2[46] = new Array('(GMT+02:00) Athens, Bucharest',								3,			5,0,3,0,0,10,5,0,4,0,0);
TIME_ZONE_LIST_V2[47] = new Array('(GMT+02:00) Jerusalem',										3,			5,5,2,0,0,9,2,0,2,0,0);
TIME_ZONE_LIST_V2[48] = new Array('(GMT+02:00) Beirut',											3,			5,6,23,59,59,10,5,4,23,59,59);
TIME_ZONE_LIST_V2[49] = new Array('(GMT+02:00) Harare, Pretoria',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[50] = new Array('(GMT+02:00) Damascus',											4,			1,4,23,59,59,10,5,4,23,59,59);
TIME_ZONE_LIST_V2[51] = new Array('(GMT+02:00) Istanbul',											3,			5,0,3,0,0,10,5,0,4,0,0);
TIME_ZONE_LIST_V2[52] = new Array('(GMT+03:00) Kuwait, Riyadh',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[53] = new Array('(GMT+03:00) Baghdad',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[54] = new Array('(GMT+03:00) Nairobi',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[55] = new Array('(GMT+03:00) Amman',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[56] = new Array('(GMT+03:00) Kaliningrad',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[57] = new Array('(GMT+03:30) Tehran',											3,			3,6,23,59,59,9,3,1,23,59,59);
TIME_ZONE_LIST_V2[58] = new Array('(GMT+04:00) Abu Dhabi, Muscat',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[59] = new Array('(GMT+04:00) Yerevan',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[60] = new Array('(GMT+04:00) Baku',												3,			5,0,4,0,0,10,5,0,5,0,0);
TIME_ZONE_LIST_V2[61] = new Array('(GMT+04:00) Tbilisi',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[62] = new Array('(GMT+04:00) Port Louis',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[63] = new Array('(GMT+04:00) Moscow, St. Petersburg, Volgograd',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[64] = new Array('(GMT+04:30) Kabul',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[65] = new Array('(GMT+05:00) Islamabad, Karachi',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[66] = new Array('(GMT+05:00) Tashkent',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[67] = new Array('(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi',				'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[68] = new Array('(GMT+05:30) Sri Jayawardenepura',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[69] = new Array('(GMT+05:45) Kathmandu',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[70] = new Array('(GMT+06:00) Dhaka',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[71] = new Array('(GMT+06:00) Astana',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[72] = new Array('(GMT+06:00) Ekaterinburg',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[73] = new Array('(GMT+06:30) Yangon (Rangoon)',									'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[74] = new Array('(GMT+07:00) Novosibirsk',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[75] = new Array('(GMT+07:00) Bangkok, Hanoi, Jakarta',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[76] = new Array('(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi',			'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[77] = new Array('(GMT+08:00) Krasnoyarsk',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[78] = new Array('(GMT+08:00) Kuala Lumpur, Singapore',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[79] = new Array('(GMT+08:00) Taipei',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[80] = new Array('(GMT+08:00) Ulaanbaatar',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[81] = new Array('(GMT+08:00) Perth',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[82] = new Array('(GMT+09:00) Seoul',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[83] = new Array('(GMT+09:00) Irkutsk',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[84] = new Array('(GMT+09:00) Osaka, Sapporo, Tokyo',							'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[85] = new Array('(GMT+09:30) Darwin',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[86] = new Array('(GMT+09:30) Adelaide',											10,			1,0,2,0,0,4,1,0,3,0,0);
TIME_ZONE_LIST_V2[87] = new Array('(GMT+10:00) Canberra, Melbourne, Sydney',						10,			1,0,2,0,0,4,1,0,3,0,0);
TIME_ZONE_LIST_V2[88] = new Array('(GMT+10:00) Brisbane',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[89] = new Array('(GMT+10:00) Hobart',											10,			1,0,2,0,0,4,1,0,3,0,0);
TIME_ZONE_LIST_V2[90] = new Array('(GMT+10:00) Guam, Port Moresby',								'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[91] = new Array('(GMT+10:00) Yakutsk',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[92] = new Array('(GMT+11:00) Solomon Is., New Caledonia',						'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[93] = new Array('(GMT+11:00) Vladivostok',										'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[94] = new Array('(GMT+12:00) Fiji',												10,			4,0,2,0,0,1,4,0,3,0,0);
TIME_ZONE_LIST_V2[95] = new Array('(GMT+12:00) Magadan',											'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[96] = new Array('(GMT+12:00) Auckland, Wellington',								9,			5,0,2,0,0,4,1,0,3,0,0);
TIME_ZONE_LIST_V2[97] = new Array('(GMT+12:00) Coordinated Universal Time+12',					'invalid',	0,0,0,0,0,0,0,0,0,0,0);
TIME_ZONE_LIST_V2[98] = new Array('(GMT+13:00) Samoa',											9,			4,6,23,59,59,4,1,0,1,0,0);
TIME_ZONE_LIST_V2[99] = new Array("(GMT+13:00) Nuku'alofa",										'invalid',	0,0,0,0,0,0,0,0,0,0,0);

var TIME_ZONE_NAME_V2 = new Array(
	"STWT12",												// 0 (GMT-12:00) International Date Line West
	"STWT11",												// 1 (GMT-11:00) Coordinated Universal Time -11
	"STWT10",												// 2 (GMT-10:00) Hawaii
	"STWT9STWST,M3.2.0/2,M11.1.0/2:0:0",					// 3 (GMT-09:00) Alaska
	"STWT8STWST,M3.2.0/2,M11.1.0/2:0:0",					// 4 (GMT-08:00) Pacific Time (USA & Canada)
	"STWT8STWST,M4.1.0/2,M10.5.0/2:0:0",					// 5 (GMT-08:00) Baja California
	"STWT7STWST,M4.1.0/2,M10.5.0/2:0:0",					// 6 (GMT-07:00) Chihuahua
	"STWT7STWST,M3.2.0/2,M11.1.0/2:0:0",					// 7 (GMT-07:00) Mountain Time(USA & Canada)
	"STWT7",												// 8 (GMT-07:00) Arizona
	"STWT6",												// 9 (GMT-06:00) Saskatchewan
	"STWT6",												//10 (GMT-06:00) Central America
	"STWT6STWST,M3.2.0/2,M11.1.0/2:0:0",					//11 (GMT-06:00) Central Time (USA & Canada)
	"STWT6STWST,M4.1.0/2,M10.5.0/2:0:0",					//12 (GMT-06:00) Guadalajara
	"STWT5STWST,M3.2.0/2,M11.1.0/2:0:0",					//13 (GMT-05:00) Eastern Time (USA & Canada)
	"STWT5",												//14 (GMT-05:00) Bogota
	"STWT5STWST,M3.2.0/2,M11.1.0/2:0:0",					//15 (GMT-05:00) Indiana (East)
	"STWT4:30",												//16 (GMT-04:30) Caracas
	"STWT4STWST,M3.2.0/2,M11.1.0/2:0:0",					//17 (GMT-04:00) Atlantic Time(Canada)
	"STWT4STWST,M10.3.6/23:59:59,M2.3.6/23:59:59",			//18 (GMT-04:00) Cuiaba
	"STWT4STWST,M10.2.6/23:59:59,M3.2.6/23:59:59",			//19 (GMT-04:00) Santiago
	"STWT4STWST,M10.1.6/23:59:59,M4.2.6/23:59:59",			//20 (GMT-04:00) Asuncion
	"STWT4",												//21 (GMT-04:00) Georgetown
	"STWT3:30STWST,M3.2.0/2,M11.1.0/2:0:0",					//22 (GMT-03:30) Newfoundland
	"STWT3",												//23 (GMT-03:00) Buenos Aires
	"STWT3",												//24 (GMT-03:00) Salbador
	"STWT3STWST,M10.3.6/23:59:59,M2.3.6/23:59:59",			//25 (GMT-03:00) Brasilia
	"STWT3STWST,M3.5.6/22,M10.5.6/23:0:0",					//26 (GMT-03:00) Greenland
	"STWT3STWST,M10.1.0/2,M3.2.0/2:0:0",					//27 (GMT-03:00) Montevideo
	"STWT3",												//28 (GMT-03:00) Cayenne
	"STWT2STWST,M3.5.0/2,M9.5.0/2:0:0",						//29 (GMT-02:00) Mid-Atlantic
	"STWT2",												//30 (GMT-02:00) Coordinated Universal Time -02
	"STWT1STWST,M3.5.6/23:59:59,M10.5.0/1:0:0",				//31 (GMT-01:00) Azores
	"STWT1",												//32 (GMT-01:00) Cape Verde Is.
	"STWT0STWST,M3.5.0/1,M10.5.0/2:0:0",					//33 (GMT) Greenwich Mean Time
	"STWT0",												//34 (GMT) Monrovia
	"STWT0STWST,M4.5.0/2,M9.5.0/3:0:0",						//35 (GMT) Casablanca
	"STWT0",												//36 (GMT) Coordinated Universal Time
	"STWT-1STWST,M3.5.0/2,M10.5.0/3:0:0",					//37 (GMT+01:00) Belgrade
	"STWT-1STWST,M3.5.0/2,M10.5.0/3:0:0",					//38 (GMT+01:00) Sarajevo
	"STWT-1STWST,M9.1.0/2,M4.1.0/2:0:0",					//39 (GMT+01:00) Windhoek
	"STWT-1STWST,M3.5.0/2,M10.5.0/3:0:0",					//40 (GMT+01:00) Brussels
	"STWT-1",												//41 (GMT+01:00) West Central Africa
	"STWT-1STWST,M3.5.0/2,M10.5.0/3:0:0",					//42 (GMT+01:00) Amsterdam
	"STWT-2STWST,M3.5.0/2,M10.5.0/3:0:0",					//43 (GMT+02:00) East Europe
	"STWT-2",												//44 (GMT+02:00) Cairo
	"STWT-2STWST,M3.5.0/3,M10.5.0/4:0:0",					//45 (GMT+02:00) Helsinki
	"STWT-2STWST,M3.5.0/3,M10.5.0/4:0:0",					//46 (GMT+02:00) Athens
	"STWT-2STWST,M3.5.5/2,M9.2.0/2:0:0",					//47 (GMT+02:00) Jerusalem
	"STWT-2STWST,M3.5.6/23:59:59,M10.5.6/23:59:59",			//48 (GMT+02:00) Beirut
	"STWT-2",												//49 (GMT+02:00) Harare
	"STWT-2STWST,M4.1.4/23:59:59,M10.5.4/23:59:59",			//50 (GMT+02:00) Damascus
	"STWT-2STWST,M3.5.0/3,M10.5.0/4:0:0",					//51 (GMT+02:00) Istanbul
	"STWT-3",												//52 (GMT+03:00) Kuwait
	"STWT-3",												//53 (GMT+03:00) Baghdad
	"STWT-3",												//54 (GMT+03:00) Nairobi
	"STWT-3",												//55 (GMT+03:00) Amman
	"STWT-3",												//56 (GMT+03:00) Kaliningrad, Minsk
	"STWT-3:30STWST,M3.3.6/23:59:59,M9.3.1/23:59:59",		//57 (GMT+03:30) Tehran
	"STWT-4",												//58 (GMT+04:00) Abu Dhabi
	"STWT-4",												//59 (GMT+04:00) Yerevan
	"STWT-4STWST,M3.5.0/4,M10.5.0/5:0:0",					//60 (GMT+04:00) Baku
	"STWT-4",												//61 (GMT+04:00) Tbilisi
	"STWT-4",												//62 (GMT+04:00) Port Louis
	"STWT-4",												//63 (GMT+04:00) Moscow
	"STWT-4:30",											//64 (GMT+04:30) Kabul
	"STWT-5",												//65 (GMT+05:00) Islamabad
	"STWT-5",												//66 (GMT+05:00) Tashkent
	"STWT-5:30",											//67 (GMT+05:30) Chennai
	"STWT-5:30",											//68 (GMT+05:30) Sri Jayawardenepura
	"STWT-5:45",											//79 (GMT+05:45) Kathmandu
	"STWT-6",												//70 (GMT+06:00) Dhaka
	"STWT-6",												//71 (GMT+06:00) Astana
	"STWT-6",												//72 (GMT+06:00) Ekaterinburg
	"STWT-6:30",											//73 (GMT+06:30) Yangon (Rangoon)
	"STWT-7",												//74 (GMT+07:00) Novosibirsk
	"STWT-7",												//75 (GMT+07:00) Bangkok
	"STWT-8",												//76 (GMT+08:00) Beijing
	"STWT-8",												//77 (GMT+08:00) Krasnoyarsk
	"STWT-8",												//78 (GMT+08:00) Kuala Lumpur
	"STWT-8",												//79 (GMT+08:00) Taipei
	"STWT-8",												//80 (GMT+08:00) Ulaanbaatar
	"STWT-8",												//81 (GMT+08:00) Perth
	"STWT-9",												//82 (GMT+09:00) Seoul
	"STWT-9",												//83 (GMT+09:00) Irkutsk
	"STWT-9",												//84 (GMT+09:00) Osaka
	"STWT-9:30",											//85 (GMT+09:30) Darwin
	"STWT-9:30STWST,M10.1.0/2,M4.1.0/3:0:0",				//86 (GMT+09:30) Adelaide
	"STWT-10STWST,M10.1.0/2,M4.1.0/3:0:0",					//87 (GMT+10:00) Canberra
	"STWT-10",												//88 (GMT+10:00) Brisbane
	"STWT-10STWST,M10.1.0/2,M4.1.0/3:0:0",					//89 (GMT+10:00) Hobart
	"STWT-10",												//90 (GMT+10:00) Guam
	"STWT-10",												//91 (GMT+10:00) Yakutsk
	"STWT-11",												//92 (GMT+11:00) Solomon Island
	"STWT-11",												//93 (GMT+11:00) Vladivostok
	"STWT-12STWST,M10.4.0/2,M1.4.0/3:0:0",					//94 (GMT+12:00) Fiji
	"STWT-12",												//95 (GMT+12:00) Magadan
	"STWT-12STWST,M9.5.0/2,M4.1.0/3:0:0",					//96 (GMT+12:00) Auckland
	"STWT-12",												//97 (GMT+12:00) Coordinated Universal Time +12
	"STWT-13STWST,M9.4.6/23:59:59,M4.1.0/1:0:0",			//98 (GMT+13:00) Samoa
	"STWT-13",												//99(GMT+13:00) Nukualofa
	""														// Custom (User-Defined) Timezone
);