import { NewsItem } from "./types";
export type { Locale, LocalizedText, NewsItem } from "./types";

// ─── AI & Frontier Science ──────────────────────────────────────────
export const aiNews: NewsItem[] = [
  {
    id: "ai-1",
    title: {
      zh: "GPT-5 发布：多模态推理能力大幅跃升",
      en: "GPT-5 Released: A Massive Leap in Multimodal Reasoning",
      de: "GPT-5 veröffentlicht: Großer Sprung im multimodalen Denken",
    },
    summary: {
      zh: "OpenAI 正式发布 GPT-5，新模型在数学、代码生成和视觉理解任务上超越前代约40%。最大亮点是其「链式推理」能力，可以分步骤解决复杂的多学科问题。该模型已向 ChatGPT Plus 用户开放。",
      en: "OpenAI has officially released GPT-5. The new model surpasses its predecessor by roughly 40% on math, code generation, and visual understanding tasks. Its headline feature is 'chain-of-thought reasoning,' allowing it to solve complex, multi-disciplinary problems step-by-step. The model is now available to ChatGPT Plus subscribers.",
      de: "OpenAI hat GPT-5 offiziell veröffentlicht. Das neue Modell übertrifft seinen Vorgänger um etwa 40 % bei Mathematik, Codegenerierung und visuellem Verständnis. Das Highlight ist die 'Ketten-Denk-Fähigkeit', die es ermöglicht, komplexe, interdisziplinäre Probleme schrittweise zu lösen. Das Modell ist jetzt für ChatGPT-Plus-Abonnenten verfügbar.",
    },
    source: "OpenAI Blog",
    date: "2026-03-03",
  },
  {
    id: "ai-2",
    title: {
      zh: "DeepMind AlphaFold 3 解锁药物-蛋白质相互作用预测",
      en: "DeepMind AlphaFold 3 Unlocks Drug–Protein Interaction Prediction",
      de: "DeepMind AlphaFold 3 entschlüsselt Wirkstoff-Protein-Interaktionen",
    },
    summary: {
      zh: "Google DeepMind 发布 AlphaFold 3，首次能够精确预测小分子药物与蛋白质的结合方式，准确率达到实验级别。这将大幅缩短新药研发周期，预计可节省数十亿美元的研发成本。",
      en: "Google DeepMind released AlphaFold 3, which for the first time can accurately predict how small-molecule drugs bind to proteins at experimental-level accuracy. This could drastically shorten drug development timelines and save billions in R&D costs.",
      de: "Google DeepMind hat AlphaFold 3 veröffentlicht, das erstmals die Bindung kleiner Moleküle an Proteine mit experimenteller Genauigkeit vorhersagen kann. Dies könnte die Arzneimittelentwicklung erheblich beschleunigen und Milliarden an F&E-Kosten einsparen.",
    },
    source: "Nature",
    date: "2026-03-02",
  },
  {
    id: "ai-3",
    title: {
      zh: "欧盟AI法案正式生效，全球进入AI监管新纪元",
      en: "EU AI Act Takes Effect, Ushering in a New Era of Global AI Regulation",
      de: "EU-KI-Gesetz tritt in Kraft und leitet eine neue Ära der KI-Regulierung ein",
    },
    summary: {
      zh: "欧盟《人工智能法案》于本月正式全面生效，将AI系统按风险等级分为四类，对高风险AI应用（如医疗诊断、自动驾驶）实施严格的透明度和审计要求。全球科技公司正紧急调整合规策略。",
      en: "The EU's Artificial Intelligence Act has come into full force this month. It classifies AI systems into four risk tiers and imposes strict transparency and audit requirements on high-risk AI applications such as medical diagnosis and autonomous driving. Global tech companies are urgently adjusting their compliance strategies.",
      de: "Das KI-Gesetz der EU ist diesen Monat vollständig in Kraft getreten. Es klassifiziert KI-Systeme in vier Risikostufen und erlegt Hochrisiko-KI-Anwendungen wie medizinischer Diagnostik und autonomem Fahren strenge Transparenz- und Prüfanforderungen auf. Weltweit passen Technologieunternehmen ihre Compliance-Strategien an.",
    },
    source: "Reuters",
    date: "2026-03-01",
  },
];

// ─── Global Politics ────────────────────────────────────────────────
export const politicsNews: NewsItem[] = [
  {
    id: "pol-1",
    title: {
      zh: "美中就半导体出口管制展开新一轮谈判",
      en: "US and China Begin New Round of Semiconductor Export Control Talks",
      de: "USA und China beginnen neue Runde der Halbleiter-Exportkontrollgespräche",
    },
    summary: {
      zh: "美国商务部长与中国工信部部长在日内瓦举行闭门会谈，讨论放宽对华芯片出口限制的可能性。双方在先进制程芯片的定义上存在分歧，但同意建立定期沟通机制。市场对此反应积极，芯片股普遍上涨。",
      en: "The US Commerce Secretary and China's Minister of Industry met behind closed doors in Geneva to discuss the possibility of easing chip export restrictions to China. Both sides disagree on the definition of 'advanced-node chips' but agreed to establish a regular communication mechanism. Markets reacted positively, with chip stocks broadly rising.",
      de: "Der US-Handelsminister und Chinas Industrieminister trafen sich in Genf hinter verschlossenen Türen, um eine mögliche Lockerung der Chip-Exportbeschränkungen nach China zu besprechen. Beide Seiten sind sich bei der Definition von 'fortschrittlichen Chips' uneinig, vereinbarten aber einen regelmäßigen Kommunikationsmechanismus. Die Märkte reagierten positiv.",
    },
    source: "Financial Times",
    date: "2026-03-03",
  },
  {
    id: "pol-2",
    title: {
      zh: "乌克兰和平峰会在维也纳举行，俄方首次派代表出席",
      en: "Ukraine Peace Summit Held in Vienna; Russia Sends Representative for the First Time",
      de: "Ukraine-Friedensgipfel in Wien: Russland entsendet erstmals einen Vertreter",
    },
    summary: {
      zh: "在联合国斡旋下，乌克兰和平峰会在维也纳召开。俄罗斯首次派出副外长级别代表出席，被视为重大外交突破。会议讨论了停火框架、领土问题和战后重建。多方签署了一份不具约束力的原则声明。",
      en: "Under UN mediation, a Ukraine peace summit was held in Vienna. Russia sent a deputy foreign minister-level representative for the first time, viewed as a major diplomatic breakthrough. The summit discussed ceasefire frameworks, territorial issues, and post-war reconstruction. Multiple parties signed a non-binding statement of principles.",
      de: "Unter UN-Vermittlung fand in Wien ein Ukraine-Friedensgipfel statt. Russland entsandte erstmals einen Vertreter auf stellvertretender Außenministerebene — ein diplomatischer Durchbruch. Der Gipfel erörterte Waffenstillstands-Rahmen, Territorialfragen und den Wiederaufbau nach dem Krieg.",
    },
    source: "BBC News",
    date: "2026-03-02",
  },
  {
    id: "pol-3",
    title: {
      zh: "印度宣布2028年载人登月计划",
      en: "India Announces Crewed Lunar Mission for 2028",
      de: "Indien kündigt bemannte Mondmission für 2028 an",
    },
    summary: {
      zh: "印度总理莫迪宣布，印度空间研究组织（ISRO）将在2028年前实施载人登月任务，成为继美国和中国之后第三个实现该目标的国家。这一计划将获得约50亿美元的专项预算，并与法国航天局开展合作。",
      en: "Indian PM Modi announced that ISRO will carry out a crewed lunar landing by 2028, making India the third country to achieve this after the US and China. The mission will receive a dedicated budget of approximately $5 billion and will involve collaboration with France's space agency CNES.",
      de: "Indiens Premierminister Modi kündigte an, dass die ISRO bis 2028 eine bemannte Mondlandung durchführen wird — Indien wäre damit das dritte Land nach den USA und China. Die Mission erhält ein Budget von etwa 5 Milliarden Dollar und wird in Zusammenarbeit mit der französischen Raumfahrtagentur CNES durchgeführt.",
    },
    source: "The Hindu",
    date: "2026-03-01",
  },
];

// ─── Stock Market ───────────────────────────────────────────────────
export const stockNews: NewsItem[] = [
  {
    id: "stk-1",
    title: {
      zh: "美股三大指数齐创新高，科技板块领涨",
      en: "All Three US Indices Hit Record Highs, Led by Tech",
      de: "Alle drei US-Indizes auf Rekordhoch, Technologie führt",
    },
    summary: {
      zh: "受AI相关企业财报超预期推动，标普500、纳斯达克和道琼斯指数同时创下历史新高。英伟达股价单日上涨8%，市值突破4万亿美元大关。分析师警告短期估值过高，建议投资者注意回调风险。",
      en: "Driven by better-than-expected AI-related earnings, the S&P 500, Nasdaq, and Dow Jones all hit record highs simultaneously. Nvidia rose 8% in a single day, pushing its market cap past $4 trillion. Analysts warn of short-term overvaluation and advise investors to watch for pullback risks.",
      de: "Getrieben von über den Erwartungen liegenden KI-Quartalszahlen erreichten S&P 500, Nasdaq und Dow Jones gleichzeitig Rekordhöhen. Nvidia stieg an einem Tag um 8 % und durchbrach die 4-Billionen-Dollar-Marke. Analysten warnen vor kurzfristiger Überbewertung.",
    },
    source: "Bloomberg",
    date: "2026-03-03",
  },
  {
    id: "stk-2",
    title: {
      zh: "比特币突破12万美元，机构资金持续涌入",
      en: "Bitcoin Surpasses $120K as Institutional Money Keeps Flowing In",
      de: "Bitcoin durchbricht 120.000 $, institutionelles Geld fließt weiter",
    },
    summary: {
      zh: "比特币价格首次突破12万美元，主要受美国多只比特币现货ETF持续吸金推动。贝莱德旗下IBIT基金单周净流入超20亿美元。以太坊同步走强，突破6000美元。加密市场总市值达到5.2万亿美元。",
      en: "Bitcoin surpassed $120,000 for the first time, mainly driven by continued inflows into multiple US spot Bitcoin ETFs. BlackRock's IBIT fund saw over $2 billion in net weekly inflows. Ethereum also surged past $6,000. The total crypto market cap reached $5.2 trillion.",
      de: "Bitcoin hat erstmals die 120.000-Dollar-Marke überschritten, angetrieben von anhaltenden Zuflüssen in US-Bitcoin-Spot-ETFs. BlackRocks IBIT-Fonds verzeichnete wöchentliche Nettozuflüsse von über 2 Mrd. $. Ethereum stieg ebenfalls über 6.000 $. Die gesamte Krypto-Marktkapitalisierung erreichte 5,2 Billionen Dollar.",
    },
    source: "CoinDesk",
    date: "2026-03-02",
  },
  {
    id: "stk-3",
    title: {
      zh: "日本央行加息至0.75%，日元大幅走强",
      en: "Bank of Japan Raises Rate to 0.75%; Yen Strengthens Sharply",
      de: "Bank of Japan erhöht Zinssatz auf 0,75 %; Yen wertet stark auf",
    },
    summary: {
      zh: "日本央行继续收紧货币政策，将基准利率上调至0.75%，为2008年以来最高水平。日元兑美元汇率快速升值至138，日经225指数应声下跌2.3%。出口导向型企业股价受到压力，但银行股受益上涨。",
      en: "The Bank of Japan continued tightening monetary policy, raising the benchmark rate to 0.75% — the highest since 2008. The yen rapidly appreciated to 138 against the dollar, while the Nikkei 225 fell 2.3%. Export-oriented stocks came under pressure, but banking stocks rallied.",
      de: "Die Bank of Japan hat die Geldpolitik weiter gestrafft und den Leitzins auf 0,75 % angehoben — den höchsten Stand seit 2008. Der Yen wertete schnell auf 138 gegenüber dem Dollar auf, der Nikkei 225 fiel um 2,3 %. Exportorientierte Aktien gerieten unter Druck, Bankaktien profitierten.",
    },
    source: "Nikkei Asia",
    date: "2026-03-01",
  },
];
