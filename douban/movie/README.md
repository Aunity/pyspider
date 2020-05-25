### <center>爬取豆瓣电影</center>
#### 1，获取电影分类
每类电影对应一个ID，ID后续用于查询该类电影。
  - Request URL: https://movie.douban.com/chart
  - Submit Method: get
  - Parse method:
    - '//*[@id="content"]/div/div[2]/div[1]/div/span' get the span list, with every span is a type of movie
    - './a/text()' get the type name from the type sapn
    - './a/@href'  get the type id from the href
    ```
    剧情 11 喜剧 24 动作 5 爱情 13 科幻 17 动画 25 悬疑 10 惊悚 19 恐怖 20 纪录片 1 短片 23 情色 6 同性 26 音乐 14 歌舞 7 家庭 28 儿童 8 传记 2 历史 4 战争 22 犯罪 3 西部 27 奇幻 16 冒险 15 灾难 12 武侠 29 古装 30 运动 18 黑色电影 31
    ```
   - 数据存储 list 并创建文件夹
   
#### 2，对每个类别进行爬取 
对每类电影进行爬取，需要依据电影评分，分段（100:90, 90:80, ... , 10:0）进行爬取。interval_id用来代表分段信息，100:90代表评分在100%~90%之间。
  - 获取某分段该类电影的数目
    - URL:https://movie.douban.com/j/chart/top_list_count
    - Submit Methods: get
    - parameters:
    ```
    paras = {
      "type": "",
      "interval_id": "100:90"
    }
    ```
    - return: json
    ```json
    {
	  "playable_count": 414,
	  "total": 697,
	  "unwatched_count": 697
    }
    ```
  - 对某分段该类电影进行爬取
    - URL: https://movie.douban.com/j/chart/top_list
    - Submit methods: get
    - parameters:
    ```dict
    paras = {
      "type": "11",
      "interval_id": "100:90",
      "action": "",
      "start": "0",
      "limit": "20"
    }
    ```
    - return: json
    ```json
    [{
	"rating": ["9.7", "50"],
	"rank": 1,
	"cover_url": "https://img3.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p480747492.jpg",
	"is_playable": true,
	"id": "1292052",
	"types": ["犯罪", "剧情"],
	"regions": ["美国"],
	"title": "肖申克的救赎",
	"url": "https:\/\/movie.douban.com\/subject\/1292052\/",
	"release_date": "1994-09-10",
	"actor_count": 25,
	"vote_count": 2022125,
	"score": "9.7",
	"actors": ["蒂姆·罗宾斯", "摩根·弗里曼", "鲍勃·冈顿", "威廉姆·赛德勒", "克兰西·布朗", "吉尔·贝罗斯", "马克·罗斯顿", "詹姆斯·惠特摩", "杰弗里·德曼", "拉里·布兰登伯格", "尼尔·吉恩托利", "布赖恩·利比", "大卫·普罗瓦尔", "约瑟夫·劳格诺", "祖德·塞克利拉", "保罗·麦克兰尼", "芮妮·布莱恩", "阿方索·弗里曼", "V·J·福斯特", "弗兰克·梅德拉诺", "马克·迈尔斯", "尼尔·萨默斯", "耐德·巴拉米", "布赖恩·戴拉特", "唐·麦克马纳斯"],
	"is_watched": false
    }]
    ```
    - 数据存储 csv格式，每个interval_id一个csv文件