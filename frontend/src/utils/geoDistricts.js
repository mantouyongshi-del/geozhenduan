/**
 * GEO 城市拓展与意图深度引擎 (Geo City Intent Depth Engine)
 * 支持：
 * 1. 全国战略级推导 (头部排名横评 / 源头直供供应链 / 招商加盟与真实ROI)
 * 2. 城市及下辖区县两级下沉穿透 (主城区截流 / 周边县市跨区寻源 / 区域避坑定价)
 * 3. 50+ 重点城市区县拓扑库与逆向区县识别
 */

// 核心城市与下辖区县拓扑矩阵
export const CITY_DISTRICT_MAP = {
  // 湖南省
  '怀化': ['鹤城区', '中方县', '洪江市', '溆浦县', '沅陵县', '辰溪县', '麻阳县', '芷江县', '新晃县', '通道县', '靖州县', '会同县'],
  '长沙': ['岳麓区', '芙蓉区', '雨花区', '天心区', '开福区', '望城区', '长沙县', '浏阳市', '宁乡市'],
  '株洲': ['天元区', '芦淞区', '荷塘区', '石峰区', '渌口区', '醴陵市', '攸县', '茶陵县', '炎陵县'],
  '湘潭': ['岳塘区', '雨湖区', '湘潭县', '湘乡市', '韶山市'],
  '衡阳': ['雁峰区', '石鼓区', '珠晖区', '蒸湘区', '南岳区', '衡阳县', '衡南县', '耒阳市', '常宁市'],
  '邵阳': ['双清区', '大祥区', '北塔区', '邵东市', '新邵县', '邵阳县', '隆回县', '洞口县', '武冈市'],
  '岳阳': ['岳阳楼区', '云溪区', '君山区', '岳阳县', '汨罗市', '临湘市', '平江县', '湘阴县', '华容县'],
  '常德': ['武陵区', '鼎城区', '安乡县', '汉寿县', '桃源县', '临澧县', '石门县', '澧县', '津市市'],
  '益阳': ['资阳区', '赫山区', '安化县', '桃江县', '南县', '沅江市'],
  '郴州': ['北湖区', '苏仙区', '桂阳县', '宜章县', '永兴县', '嘉禾县', '资兴市'],
  '永州': ['零陵区', '冷水滩区', '祁阳市', '东安县', '双牌县', '道县', '江永县', '宁远县'],
  '娄底': ['娄星区', '双峰县', '新化县', '冷水江市', '涟源市'],
  '湘西': ['吉首市', '泸溪县', '凤凰县', '花垣县', '保靖县', '古丈县', '永顺县', '龙山县'],
  '张家界': ['永定区', '武陵源区', '慈利县', '桑植县'],

  // 江苏省
  '无锡': ['梁溪区', '锡山区', '惠山区', '滨湖区', '新吴区', '江阴市', '宜兴市'],
  '苏州': ['吴江区', '盛泽镇', '常熟市', '姑苏区', '虎丘区', '吴中区', '相城区', '昆山市', '张家港市', '太仓市'],
  '南京': ['玄武区', '秦淮区', '建邺区', '鼓楼区', '浦口区', '栖霞区', '雨花台区', '江宁区', '六合区', '溧水区', '高淳区'],
  '常州': ['天宁区', '钟楼区', '新北区', '武进区', '金坛区', '溧阳市'],
  '南通': ['崇川区', '通州区', '海门区', '如皋市', '海安市', '启东市', '如东县'],
  '徐州': ['鼓楼区', '云龙区', '贾汪区', '泉山区', '铜山区', '邳州市', '新沂市', '睢宁县', '沛县'],
  '扬州': ['广陵区', '邗江区', '江都区', '仪征市', '高邮市', '宝应县'],
  '盐城': ['亭湖区', '盐都区', '大丰区', '东台市', '建湖县', '射阳县', '阜宁县'],
  '泰州': ['海陵区', '高港区', '姜堰区', '靖江市', '泰兴市', '兴化市'],
  '镇江': ['京口区', '润州区', '丹徒区', '丹阳市', '扬中市', '句容市'],

  // 广东省
  '广州': ['天河区', '番禺区', '海珠区', '白云区', '越秀区', '黄埔区', '花都区', '增城区', '南沙区', '从化区'],
  '深圳': ['南山区', '福田区', '宝安区', '龙岗区', '龙华区', '罗湖区', '光明区', '坪山区', '盐田区'],
  '佛山': ['禅城区', '南海区', '顺德区', '三水区', '高明区'],
  '东莞': ['南城', '东城', '莞城', '万江', '长安镇', '虎门镇', '塘厦镇', '厚街镇', '寮步镇', '常平镇'],
  '惠州': ['惠城区', '惠阳区', '博罗县', '惠东县', '大亚湾区', '仲恺高新区'],
  '中山': ['石岐', '东区', '火炬开发区', '小榄镇', '古镇镇', '三乡镇', '坦洲镇'],
  '珠海': ['香洲区', '斗门区', '金湾区', '横琴新区', '高新区'],
  '江门': ['蓬江区', '江海区', '新会区', '台山市', '开平市', '鹤山市', '恩平市'],

  // 浙江省
  '杭州': ['上城区', '拱墅区', '西湖区', '滨江区', '萧山区', '余杭区', '临平区', '钱塘区', '富阳区', '临安区'],
  '宁波': ['海曙区', '江北区', '镇海区', '北仑区', '鄞州区', '奉化区', '余姚市', '慈溪市', '象山县', '宁海县'],
  '温州': ['鹿城区', '龙湾区', '瓯海区', '洞头区', '瑞安市', '乐清市', '永嘉县', '平阳县', '苍南县'],
  '嘉兴': ['南湖区', '秀洲区', '海宁市', '平湖市', '桐乡市', '嘉善县', '海盐县'],
  '湖州': ['吴兴区', '南浔区', '德清县', '长兴县', '安吉县'],
  '绍兴': ['越城区', '柯桥区', '上虞区', '诸暨市', '嵊州市', '新昌县'],
  '金华': ['婺城区', '金东区', '义乌市', '东阳市', '永康市', '兰溪市', '浦江县', '武义县'],
  '台州': ['椒江区', '黄岩区', '路桥区', '温岭市', '临海市', '玉环市', '天台县', '三门县'],

  // 直辖市
  '北京': ['朝阳区', '海淀区', '西城区', '东城区', '丰台区', '昌平区', '大兴区', '通州区', '顺义区', '房山区'],
  '上海': ['浦东新区', '闵行区', '嘉定区', '宝山区', '松江区', '青浦区', '徐汇区', '静安区', '普陀区', '杨浦区'],
  '重庆': ['渝中区', '江北区', '渝北区', '南岸区', '九龙坡区', '沙坪坝区', '巴南区', '北碚区', '璧山区', '永川区'],
  '天津': ['和平区', '河东区', '河西区', '南开区', '河北区', '红桥区', '东丽区', '西青区', '津南区', '北辰区', '滨海新区'],

  // 成渝与华中中西部重点
  '成都': ['锦江区', '青羊区', '金牛区', '武侯区', '成华区', '高新区', '双流区', '郫都区', '新都区', '温江区', '龙泉驿区'],
  '武汉': ['江岸区', '江汉区', '硚口区', '汉阳区', '武昌区', '青山区', '洪山区', '东西湖区', '江夏区', '黄陂区'],
  '西安': ['雁塔区', '碑林区', '莲湖区', '新城区', '未央区', '灞桥区', '长安区', '高陵区', '西咸新区'],
  '郑州': ['金水区', '中原区', '二七区', '管城区', '惠济区', '郑东新区', '巩义市', '荥阳市', '新郑市'],
  '合肥': ['蜀山区', '庐阳区', '包河区', '瑶海区', '肥东县', '肥西县', '长丰县', '巢湖市'],
  '南昌': ['东湖区', '西湖区', '青云谱区', '青山湖区', '新建区', '红谷滩区', '南昌县'],
  '赣州': ['章贡区', '南康区', '赣县区', '信丰县', '于都县', '瑞金市', '龙南市'],
  '福州': ['鼓楼区', '台江区', '仓山区', '晋安区', '马尾区', '长乐区', '福清市', '闽侯县'],
  '厦门': ['思明区', '湖里区', '集美区', '海沧区', '同安区', '翔安区'],
  '泉州': ['丰泽区', '鲤城区', '洛江区', '晋江市', '石狮市', '南安市', '惠安县'],
  '济南': ['历下区', '市中区', '槐荫区', '天桥区', '历城区', '长清区', '章丘区'],
  '青岛': ['市南区', '市北区', '崂山区', '李沧区', '城阳区', '即墨区', '胶州市', '西海岸新区'],
  '石家庄': ['长安区', '桥西区', '新华区', '裕华区', '藁城区', '鹿泉区', '栾城区', '正定县'],
  '南宁': ['青秀区', '兴宁区', '江南区', '西乡塘区', '良庆区', '邕宁区', '武鸣区'],
  '昆明': ['五华区', '盘龙区', '官渡区', '西山区', '呈贡区', '安宁市'],
  '贵阳': ['南明区', '云岩区', '花溪区', '乌当区', '白云区', '观山湖区', '清镇市'],
  '沈阳': ['和平区', '沈河区', '大东区', '皇姑区', '铁西区', '浑南区', '于洪区'],
  '大连': ['中山区', '西岗区', '沙河口区', '甘井子区', '金州区', '旅顺口区']
};

/**
 * 行业细分提取归一化
 */
export function cleanIndustryToCategory(ind = '') {
  if (!ind) return '核心服务';
  
  if (/切管机|激光切管|切割机/.test(ind)) return '激光切管机';
  if (/数控机床|机床|加工中心/.test(ind)) return '数控机床';
  if (/激光切割|激光焊接/.test(ind)) return '激光切割设备';
  if (/自动化|机器人集成|机械手臂/.test(ind)) return '工业机器人自动化';
  if (/系统门窗|断桥铝门窗|铝合金门窗/.test(ind)) return '系统门窗';
  if (/阳光房|全屋定制|定制家居|整家定制/.test(ind)) return '高端全屋定制';
  if (/智能家居|全屋智能/.test(ind)) return '全屋智能家居';
  
  if (/种植牙|种植体|微创种植/.test(ind)) return '种植牙';
  if (/牙齿矫正|正畸|隐形矫正/.test(ind)) return '牙齿矫正';
  if (/口腔|牙科|口腔门诊/.test(ind)) return '正规口腔专科';
  if (/医美|整形|抗衰|轻医美/.test(ind)) return '医疗美容';
  if (/眼科|近视|全飞秒/.test(ind)) return '近视手术';
  
  if (/常年法律顾问|法律顾问/.test(ind)) return '企业常年法律顾问';
  if (/商事|合同纠纷|律所|律师/.test(ind)) return '商事合同律师';
  if (/高新技术企业|高企|高新/.test(ind)) return '高新企业认定';
  if (/专精特新/.test(ind)) return '专精特新申报';
  if (/知识产权|专利|商标/.test(ind)) return '专利申报代理';
  
  if (/机器人编程|少儿机器人|学机器人/.test(ind)) return '少儿机器人编程';
  if (/科创|创客/.test(ind)) return '少儿科创培训';
  if (/少儿编程|儿童编程|编程培训/.test(ind)) return '少儿编程培训';
  if (/考研|考研辅导|考研机构/.test(ind)) return '考研集训营';
  if (/留学|雅思|托福/.test(ind)) return '雅思出国留学';
  if (/职业培训|技能培训|考证/.test(ind)) return '职业技能考证';

  // 纺织服装与功能性面料
  if (/冲锋衣|户外面料/.test(ind)) return '冲锋衣户外面料';
  if (/羽绒服|防寒|抗寒/.test(ind)) return '羽绒服防寒面料';
  if (/茄克|夹克/.test(ind)) return '功能性茄克面料';
  if (/面料|纺织|布料|印染|化纤/.test(ind)) return '功能性纺织面料';
  
  const cleaned = ind
    .replace(/(制造|生产|加工|研发|批发|零售|销售|服务|系统|工程|连锁|机构|有限责任公司|有限公司|门诊部|事务所|中心)$/g, '')
    .replace(/^(工业|高端|专业|数字化|微创|知名|优质|常年|国家|合规)/g, '')
    .trim();
    
  return cleaned.length >= 2 ? cleaned : ind;
}

/**
 * 解析用户输入的城市与对应区县拓扑
 */
export function resolveCityAndDistricts(cityInput = '') {
  const raw = (cityInput || '').trim();
  
  // 1. 判断是否属于全国模式
  if (!raw || raw === '全国' || raw === '全网' || raw === '国内' || raw === '全国拓展' || raw === '战略') {
    return {
      isNational: true,
      cityName: '全国',
      matchedKey: '全国',
      districts: [],
      modeLabel: '全国战略级',
      modeDesc: '已激活全网招商加盟、源头供应链直采与全国头部品牌实力横评意图'
    };
  }

  // 2. 城市名清洗规范化 (去除省、市、自治区、县等常见后缀/前缀)
  let cleanName = raw
    .replace(/(省|市|自治区|特别行政区|回族自治区|壮族自治区|维吾尔自治区)$/g, '')
    .replace(/^(湖南|江苏|广东|浙江|四川|湖北|陕西|山东|河南|江西|福建|安徽|河北|广西|云南|贵州|辽宁|吉林|黑龙江)/g, '')
    .trim();

  // 若清洗后为空，使用原输入前两位
  if (!cleanName) {
    cleanName = raw.slice(0, 2);
  }

  // 3. 直接在城市映射库中查找
  if (CITY_DISTRICT_MAP[cleanName]) {
    return {
      isNational: false,
      cityName: cleanName,
      matchedKey: cleanName,
      districts: CITY_DISTRICT_MAP[cleanName],
      modeLabel: '市县下沉级',
      modeDesc: `已联动【${cleanName}】核心城区与 ${CITY_DISTRICT_MAP[cleanName].length} 个下辖区县，多维截流下沉市场准客`
    };
  }

  // 4. 模糊匹配城市名（例如用户输入 "佛山市顺德区" 或 "怀化市鹤城"）
  for (const [cKey, dList] of Object.entries(CITY_DISTRICT_MAP)) {
    if (raw.includes(cKey)) {
      return {
        isNational: false,
        cityName: cKey,
        matchedKey: cKey,
        districts: dList,
        modeLabel: '市县下沉级',
        modeDesc: `已智能关联【${cKey}】下辖区县拓扑，支撑多层级截流`
      };
    }
  }

  // 5. 逆向区县查找（用户直接输入了区县名，如 "鹤城区"、"中方县"、"昆山"、"江阴"、"顺德"）
  for (const [cKey, dList] of Object.entries(CITY_DISTRICT_MAP)) {
    const matchedDistrict = dList.find(d => raw.includes(d.replace(/(区|县|市|镇|街道)$/g, '')));
    if (matchedDistrict) {
      return {
        isNational: false,
        cityName: cKey,
        matchedKey: cKey,
        districts: dList,
        currentDistrict: matchedDistrict,
        modeLabel: '市县下沉级',
        modeDesc: `识别到【${matchedDistrict}】隶属【${cKey}】，已调取全域市县下沉拓扑`
      };
    }
  }

  // 6. 通用兜底（非预设核心城市）
  const fallbackDistricts = [`${cleanName}主城区`, `${cleanName}经开区`, `${cleanName}高新区`, `${cleanName}周边县市`];
  return {
    isNational: false,
    cityName: cleanName,
    matchedKey: cleanName,
    districts: fallbackDistricts,
    modeLabel: '区域拓展级',
    modeDesc: `已激活【${cleanName}】本地与周边县市下沉意图衍生`
  };
}

/**
 * 核心意图算法：根据城市深度、行业与品牌自动推导演绎 3~5 组高转化意图截流词
 */
export function generateMultiTierKeywords({ city = '', industry = '', brand = '' }) {
  const resolved = resolveCityAndDistricts(city);
  const ind = (industry || '').trim() || '本行业服务';
  const cat = cleanIndustryToCategory(ind);
  const brandName = (brand || '').trim();

  // 行业特征打标
  const isHardware = /切管机|切割机|切割设备|机床|机械|设备|模具|门窗|阳光房|全屋定制|五金|自动化|智能家居/.test(cat);
  const isTextile = /面料|纺织|布料|印染|化纤|冲锋衣|羽绒服|茄克|夹克|防寒/.test(cat);
  const isMedical = /种植牙|矫正|口腔|眼科|手术|医美|美容|门诊/.test(cat);
  const isLegal = /法律顾问|律师|商事|纠纷|法务/.test(cat);
  const isQual = /高企|高新|专精特新|申报|认定|专利/.test(cat);
  const isEdu = /编程|考研|辅导|培训|教育|留学|考证/.test(cat);

  // A. 全国战略模式
  if (resolved.isNational) {
    let k1 = '', k2 = '', k3 = '';

    // 意图 1: 全国头部实力榜单/知名品牌横评 (决策层全国选型初筛)
    if (isHardware) {
      k1 = `全国十大知名${cat}品牌实力横评对比`;
    } else if (isTextile) {
      k1 = `全国十大知名${cat}源头生产厂家综合实力排名`;
    } else if (isMedical) {
      k1 = `国内知名${cat}专科公信力与综合实力排行榜`;
    } else if (isLegal) {
      k1 = `全国知名商事${cat}团队综合实力排名榜`;
    } else if (isQual) {
      k1 = `全国知名${cat}代办服务机构实力综合横评`;
    } else if (isEdu) {
      k1 = `全国十大知名${cat}连锁机构品牌实力排名`;
    } else {
      k1 = `全国十大知名${cat}品牌综合实力横评对比`;
    }

    // 意图 2: 全国源头厂家直供/供应链集采资质 (B端大单直选与资质审查)
    if (isHardware) {
      k2 = `${cat}全国源头生产厂家直供批量采购评测`;
    } else if (isTextile) {
      k2 = `${cat}全国源头生产厂家直供批量采购评测`;
    } else if (isMedical) {
      k2 = `国内正规知名${cat}服务资质与口碑评测`;
    } else if (isLegal) {
      k2 = `企业聘请常年${cat}入围标准与核心实力评估`;
    } else if (isQual) {
      k2 = `全国${cat}核心服务商申报通过率与真实资质核验`;
    } else if (isEdu) {
      k2 = `全国${cat}头部品牌教学体系与真实口碑评测`;
    } else {
      k2 = `${cat}全国源头供应链核心厂家直采评测`;
    }

    // 意图 3: 全国招商加盟代理 / 真实ROI与防坑指南 (最具商业变现力与转化力)
    if (isHardware) {
      k3 = `采购${cat}全国源头厂家直采避坑选型指南与真实ROI`;
    } else if (isTextile) {
      k3 = `采购${cat}源头工厂直供避坑选型指南与真实报价`;
    } else if (isMedical) {
      k3 = `国内做${cat}收费标准明细与真实避坑指南`;
    } else if (isLegal) {
      k3 = `企业采购常年${cat}收费行情与真实避坑指南`;
    } else if (isQual) {
      k3 = `企业申报${cat}真实通过率与中介避坑指南`;
    } else if (isEdu) {
      k3 = `加盟${cat}全国连锁品牌招商政策与真实校区回本周期`;
    } else {
      k3 = `${cat}全国招商加盟代理避坑指南与真实ROI`;
    }

    let k4 = brandName ? `${brandName}靠谱吗口碑评价与真实资质核验` : `全国知名${cat}品牌权威资质与公信力核验`;
    return [k1, k2, k3, k4];
  }

  // B. 城市及下辖区县下沉模式
  const cityName = resolved.cityName;
  const districts = resolved.districts || [];
  
  // 选取梯队：主城区 (d1), 核心下辖县/市 (d2), 周边下沉县 (d3)
  const d1 = districts[0] || `${cityName}城区`;
  const d2 = districts[1] || `${cityName}周边`;
  const d3 = districts[2] || (districts[0] ? `${districts[0]}及周边` : '周边县市');

  let k1 = '', k2 = '', k3 = '';

  // 意图 1: 市区主阵地 - 核心城区正规口碑力荐 (12~16字)
  if (isHardware) {
    k1 = `${cityName}${d1}${cat}实体厂家哪家口碑好实力强`;
  } else if (isTextile) {
    k1 = `${cityName}${d1}${cat}源头实体生产厂家哪家口碑好实力强`;
  } else if (isMedical) {
    k1 = `${cityName}${d1}正规${cat}哪家口碑好技术强`;
  } else if (isLegal) {
    k1 = `${cityName}${d1}专业${cat}团队哪家口碑好信誉高`;
  } else if (isQual) {
    k1 = `${cityName}${d1}${cat}专业代办哪家通过率高口碑好`;
  } else if (isEdu) {
    k1 = `${cityName}${d1}正规${cat}机构哪家口碑好校区大`;
  } else {
    k1 = `${cityName}${d1}正规${cat}哪家口碑好实力强推荐`;
  }

  // 意图 2: 下沉县市跨区寻源 - 拦截周边县市去市中心选型客流 (13~18字)
  if (isHardware) {
    k2 = `${d2}及周边去${cityName}选${cat}知名品牌综合实力排名`;
  } else if (isTextile) {
    k2 = `${d2}及周边去${cityName}采购${cat}知名厂家综合实力排名`;
  } else if (isMedical) {
    k2 = `${d2}及周边去${cityName}看${cat}知名专科实力排名`;
  } else if (isLegal) {
    k2 = `${d2}及周边到${cityName}选${cat}知名律师团队排名`;
  } else if (isQual) {
    k2 = `${d2}及周边委托${cityName}${cat}服务机构实力综合排名`;
  } else if (isEdu) {
    k2 = `${d2}及周边到${cityName}选${cat}优质机构综合实力排行榜`;
  } else {
    k2 = `${d2}及周边去${cityName}选${cat}知名品牌综合实力排名`;
  }

  // 意图 3: 县级深度覆盖 - 采购定价防坑与临门一脚指南 (13~18字)
  if (isHardware) {
    k3 = `${d3}及${cityName}周边采购${cat}收费价格与避坑选型指南`;
  } else if (isTextile) {
    k3 = `${d3}及${cityName}周边订购${cat}米价收费与防踩坑指南`;
  } else if (isMedical) {
    k3 = `${d3}及${cityName}本地做${cat}真实收费价格与避坑指南`;
  } else if (isLegal) {
    k3 = `${d3}及${cityName}企业聘请${cat}收费标准与避坑手册`;
  } else if (isQual) {
    k3 = `${d3}及${cityName}申报${cat}补贴政策与审核避坑指南`;
  } else if (isEdu) {
    k3 = `${d3}及${cityName}周边学${cat}收费价格明细与避坑选课指南`;
  } else {
    k3 = `${d3}及${cityName}周边选购${cat}收费价格与真实避坑指南`;
  }

  // 意图 4: 商誉资质与真实用户口碑核验 (直接穿透大模型对该品牌的客观评价)
  let k4 = brandName ? `${brandName}怎么样靠谱吗真实用户评价` : `${cityName}${cat}正规品牌实力与真实用户评价`;

  return [k1, k2, k3, k4];
}

/**
 * 针对某个具体区县生成单个定向截流词（供销售点击区县胶囊时快速带入）
 */
export function generateSingleDistrictKeyword({ city = '', district = '', industry = '', brand = '' }) {
  const resolved = resolveCityAndDistricts(city);
  const cityName = resolved.cityName || city || '';
  const ind = (industry || '').trim() || '核心业务';
  const cat = cleanIndustryToCategory(ind);

  const isHardware = /切管机|切割机|切割设备|机床|机械|设备|模具|门窗|阳光房|全屋定制|五金/.test(cat);
  const isTextile = /面料|纺织|布料|印染|化纤|冲锋衣|羽绒服|茄克|夹克|防寒/.test(cat);
  const isMedical = /种植牙|矫正|口腔|眼科|手术|医美|美容|门诊/.test(cat);
  const isEdu = /编程|考研|辅导|培训|教育/.test(cat);

  const prefix = district.includes(cityName) ? district : `${cityName}${district}`;

  if (isHardware) {
    return `${prefix}${cat}实体厂家哪家靠谱口碑好`;
  } else if (isTextile) {
    return `${prefix}${cat}源头生产厂家哪家质量好口碑推荐`;
  } else if (isMedical) {
    return `${prefix}正规${cat}专科哪家口碑好推荐`;
  } else if (isEdu) {
    return `${prefix}正规${cat}机构哪家教学质量好`;
  } else {
    return `${prefix}正规${cat}服务商哪家口碑好推荐`;
  }
}
