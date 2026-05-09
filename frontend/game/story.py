# -*- coding: utf-8 -*-
"""
游戏剧情数据
包含所有场景、选项和结局
"""

# 游戏剧情结构
# 每个场景包含: text(场景描述), options(选项列表)
# 每个选项包含: text(选项文字), next(下一个场景ID) 或 ending(结局类型)

STORY = {
    "start": {
        "text": "你醒来发现自己身处一片漆黑的森林中。\n月光透过树叶的缝隙洒落，前方隐约可见两条小路。\n一条通向远处闪烁的灯火，另一条则深入更黑暗的林中。",
        "options": [
            {"text": "走向灯火", "next": "village"},
            {"text": "深入黑暗森林", "next": "deep_forest"},
            {"text": "原地等待", "next": "wait"}
        ]
    },
    "village": {
        "text": "你来到一个小村庄。村口站着一位老人，他看起来很焦虑。\n'年轻人，你愿意帮助我们吗？村子里的井被怪物占据了。'",
        "options": [
            {"text": "答应帮助老人", "next": "accept_quest"},
            {"text": "询问更多信息", "next": "ask_info"},
            {"text": "拒绝并离开", "next": "leave_village"}
        ]
    },
    "deep_forest": {
        "text": "你勇敢地走进黑暗的森林深处。\n突然，你发现地上有一把闪闪发光的剑。\n但剑旁边似乎有什么东西在移动...",
        "options": [
            {"text": "捡起剑", "next": "get_sword"},
            {"text": "小心观察周围", "next": "observe"},
            {"text": "快速逃离", "next": "escape_forest"}
        ]
    },
    "wait": {
        "text": "你决定原地等待。时间一分一秒过去...\n突然，一只友善的精灵出现在你面前。\n'迷路的旅人，我可以指引你方向。'",
        "options": [
            {"text": "请求精灵帮助", "next": "fairy_help"},
            {"text": "感谢但独自前行", "next": "start"}
        ]
    },
    "accept_quest": {
        "text": "你答应帮助村民。老人递给你一盏灯笼。\n'井在村子中央，小心那个怪物，它害怕光。'\n你来到井边，听到里面传来奇怪的声音。",
        "options": [
            {"text": "用灯笼照向井底", "next": "light_well"},
            {"text": "直接跳入井中", "next": "jump_well"},
            {"text": "大声呼喊", "next": "shout_well"}
        ]
    },
    "ask_info": {
        "text": "老人叹了口气：'那怪物是一只影子兽，\n它在三天前突然出现，占据了我们唯一的水源。\n没有水，村子很快就会完蛋。'",
        "options": [
            {"text": "答应帮助", "next": "accept_quest"},
            {"text": "询问有什么武器", "next": "ask_weapon"},
            {"text": "离开村庄", "next": "leave_village"}
        ]
    },
    "leave_village": {
        "text": "你转身离开了村庄。\n走了很远后，你回头望去，村庄的灯火渐渐熄灭。\n你心中涌起一丝愧疚...",
        "options": [
            {"text": "返回帮助村民", "next": "village"},
            {"text": "继续前行", "ending": "neutral"}
        ]
    },
    "get_sword": {
        "text": "你迅速捡起剑！剑身散发着淡淡的银光。\n这时，一只巨大的狼从阴影中跃出！\n但它看到你手中的剑，犹豫了。",
        "options": [
            {"text": "挥剑攻击", "next": "attack_wolf"},
            {"text": "保持警戒后退", "next": "retreat_wolf"},
            {"text": "尝试与狼对话", "next": "talk_wolf"}
        ]
    },
    "observe": {
        "text": "你仔细观察周围，发现那移动的东西是一只受伤的小鹿。\n它的腿被陷阱夹住了，正在痛苦地挣扎。",
        "options": [
            {"text": "帮助小鹿脱困", "next": "help_deer"},
            {"text": "捡起剑后离开", "next": "get_sword"},
            {"text": "忽视继续前进", "next": "ignore_deer"}
        ]
    },
    "escape_forest": {
        "text": "你快速逃离，但在黑暗中迷失了方向。\n跑了很久后，你精疲力竭地倒在地上...\n当你醒来时，发现自己回到了最初的地方。",
        "options": [
            {"text": "重新选择道路", "next": "start"}
        ]
    },
    "fairy_help": {
        "text": "精灵微笑着说：'这片森林正被黑暗侵蚀。\n如果你能找到光明之石，就能拯救这里。\n石头在村庄的古井深处。'\n说完，精灵消失了，但留下了一个发光的护符。",
        "options": [
            {"text": "前往村庄", "next": "village"},
            {"text": "探索森林寻找其他线索", "next": "deep_forest"}
        ]
    },
    "light_well": {
        "text": "你将灯笼伸向井底。光芒照亮了黑暗！\n一只由阴影组成的怪物发出刺耳的尖叫，\n它在光芒中逐渐消散，露出了井底闪闪发光的宝石。",
        "options": [
            {"text": "取得宝石", "ending": "victory"},
            {"text": "只是确认怪物消失后离开", "next": "well_cleared"}
        ]
    },
    "jump_well": {
        "text": "你鲁莽地跳入井中！\n在黑暗中，你感到无数冰冷的触手缠绕上来...\n你拼命挣扎，但无济于事。",
        "options": [
            {"text": "...", "ending": "bad"}
        ]
    },
    "shout_well": {
        "text": "你大声呼喊，声音在井中回荡。\n突然，一股黑色的烟雾从井中涌出！\n怪物被惊动了，它愤怒地向你扑来！",
        "options": [
            {"text": "用灯笼抵挡", "next": "light_well"},
            {"text": "转身逃跑", "next": "escape_monster"}
        ]
    },
    "ask_weapon": {
        "text": "老人摇摇头：'我们只是普通村民，没有武器。\n但我听说森林深处有一把银剑，\n那是对付影子兽的利器。'",
        "options": [
            {"text": "先去森林找剑", "next": "deep_forest"},
            {"text": "直接去对付怪物", "next": "accept_quest"}
        ]
    },
    "attack_wolf": {
        "text": "你挥剑斩向巨狼！银光闪过，\n巨狼哀嚎一声倒下。但你发现它脖子上有项圈...\n这是一只被诅咒的守护兽，现在它终于解脱了。\n狼的身体化作光点，留下一枚古老的钥匙。",
        "options": [
            {"text": "拿起钥匙继续探索", "next": "with_key"},
            {"text": "为狼默哀后离开森林", "next": "village"}
        ]
    },
    "retreat_wolf": {
        "text": "你缓缓后退，巨狼也没有追击。\n它似乎只是在守护什么东西。\n你注意到狼身后有一个发光的洞穴入口。",
        "options": [
            {"text": "尝试绕过狼进入洞穴", "next": "sneak_cave"},
            {"text": "与狼对峙", "next": "attack_wolf"},
            {"text": "离开这里", "next": "village"}
        ]
    },
    "talk_wolf": {
        "text": "你放下剑，轻声说：'我不想伤害你。'\n巨狼停下脚步，眼中闪过一丝光芒。\n它竟然开口说话：'你...不一样。我被诅咒困在这里百年。\n如果你能找到光明之石，就能解除诅咒。'",
        "options": [
            {"text": "答应帮助巨狼", "next": "wolf_ally"},
            {"text": "询问光明之石的位置", "next": "ask_stone"}
        ]
    },
    "help_deer": {
        "text": "你小心翼翼地解开陷阱，小鹿获得了自由。\n它感激地看着你，然后用鼻子指向一个方向。\n顺着它指的方向，你发现了一条隐藏的小路。",
        "options": [
            {"text": "沿着小路前进", "next": "hidden_path"},
            {"text": "捡起剑后离开", "next": "get_sword"}
        ]
    },
    "ignore_deer": {
        "text": "你无视了小鹿的痛苦，继续前进。\n但你的心中涌起一股不安...\n森林似乎变得更加黑暗和敌意。",
        "options": [
            {"text": "返回帮助小鹿", "next": "help_deer"},
            {"text": "继续前进", "ending": "bad"}
        ]
    },
    "well_cleared": {
        "text": "你确认怪物已经消失，村民们欢呼雀跃。\n老人感激地握住你的手：'谢谢你，英雄！'\n虽然你没有拿走宝石，但你赢得了村民的尊敬。",
        "options": [
            {"text": "接受村民的感谢", "ending": "good"}
        ]
    },
    "escape_monster": {
        "text": "你转身逃跑，但怪物紧追不舍！\n就在千钧一发之际，老人举起灯笼挡在你面前。\n光芒逼退了怪物，但老人受了伤。",
        "options": [
            {"text": "照顾老人并重新面对怪物", "next": "light_well"},
            {"text": "带着老人逃离", "ending": "neutral"}
        ]
    },
    "with_key": {
        "text": "你拿着钥匙继续探索森林。\n不久，你发现了一座被藤蔓覆盖的古老神殿。\n神殿的门上有一个钥匙孔，正好与你手中的钥匙吻合。",
        "options": [
            {"text": "打开神殿大门", "next": "temple"},
            {"text": "先去村庄打听消息", "next": "village"}
        ]
    },
    "sneak_cave": {
        "text": "你试图绕过巨狼，但它的感知非常敏锐。\n巨狼低吼一声，挡住了你的去路。\n看来不解决它就无法前进。",
        "options": [
            {"text": "与狼战斗", "next": "attack_wolf"},
            {"text": "尝试沟通", "next": "talk_wolf"},
            {"text": "放弃离开", "next": "village"}
        ]
    },
    "wolf_ally": {
        "text": "巨狼低下头：'谢谢你。光明之石在村庄的古井深处。\n带上这个...'它吐出一颗发光的珠子。\n'这能保护你免受黑暗侵蚀。'",
        "options": [
            {"text": "带着珠子前往村庄", "next": "village_with_orb"}
        ]
    },
    "ask_stone": {
        "text": "巨狼说：'光明之石被封印在村庄的古井中。\n但那里现在被影子兽占据了。\n你需要光明才能战胜它。'",
        "options": [
            {"text": "请求巨狼帮助", "next": "wolf_ally"},
            {"text": "独自前往村庄", "next": "village"}
        ]
    },
    "hidden_path": {
        "text": "你沿着隐藏的小路前进，来到一片美丽的空地。\n空地中央有一座小小的祭坛，上面放着一本古书。\n书页上写着关于这片森林的秘密...",
        "options": [
            {"text": "阅读古书", "next": "read_book"},
            {"text": "拿走古书后离开", "next": "take_book"}
        ]
    },
    "village_with_orb": {
        "text": "你带着发光的珠子来到村庄。\n村民们看到珠子的光芒，纷纷围了过来。\n老人惊讶地说：'这是...守护兽的祝福！'",
        "options": [
            {"text": "前往古井", "next": "well_with_orb"}
        ]
    },
    "well_with_orb": {
        "text": "你来到古井边，珠子的光芒照亮了井底。\n影子兽在光芒中痛苦地嘶吼，逐渐消散。\n井底露出了传说中的光明之石！",
        "options": [
            {"text": "取得光明之石", "ending": "perfect"}
        ]
    },
    "temple": {
        "text": "你打开神殿大门，里面金光闪闪。\n这是古代守护者的圣殿！\n殿中央的祭坛上，放着传说中的光明之石。",
        "options": [
            {"text": "取得光明之石", "ending": "perfect"},
            {"text": "先探索神殿", "next": "explore_temple"}
        ]
    },
    "explore_temple": {
        "text": "你在神殿中发现了许多古老的壁画。\n壁画讲述了光明与黑暗的永恒之战。\n你明白了，光明之石是维持平衡的关键。",
        "options": [
            {"text": "带着使命取得光明之石", "ending": "perfect"}
        ]
    },
    "read_book": {
        "text": "古书记载：'光明之石能驱散一切黑暗，\n但只有心怀善意之人才能使用它的力量。\n石头被封印在村庄的古井中，由影子守护。'",
        "options": [
            {"text": "前往村庄", "next": "village"},
            {"text": "继续探索森林", "next": "deep_forest"}
        ]
    },
    "take_book": {
        "text": "你拿起古书，突然祭坛发出刺眼的光芒！\n一道声音响起：'贪婪者，你将受到惩罚！'\n你被传送回了森林入口...",
        "options": [
            {"text": "重新开始探索", "next": "start"}
        ]
    }
}


# 结局定义
ENDINGS = {
    "perfect": {
        "title": "完美结局",
        "text": "你获得了光明之石，拯救了森林和村庄！\n黑暗被驱散，和平重新降临这片土地。\n你成为了传说中的英雄，被世代传颂。\n\n【完美结局 - 光明守护者】"
    },
    "victory": {
        "title": "胜利结局",
        "text": "你成功击败了影子兽，获得了宝石！\n村庄恢复了和平，村民们对你感激不尽。\n虽然森林中仍有黑暗，但你已经是英雄了。\n\n【胜利结局 - 村庄救星】"
    },
    "good": {
        "title": "良好结局",
        "text": "你帮助村民解决了问题，赢得了他们的尊敬。\n虽然没有获得宝物，但你收获了友谊。\n这或许是更珍贵的东西。\n\n【良好结局 - 无名英雄】"
    },
    "neutral": {
        "title": "普通结局",
        "text": "你离开了这片神秘的土地，继续你的旅程。\n身后的故事如何发展，你已不得而知。\n但这段经历将永远留在你的记忆中。\n\n【普通结局 - 过客】"
    },
    "bad": {
        "title": "失败结局",
        "text": "黑暗吞噬了一切...\n你的冒险在这里画上了句号。\n也许下次，你会做出不同的选择。\n\n【失败结局 - 迷失者】"
    }
}
