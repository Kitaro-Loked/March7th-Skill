import random
from openclaw.sdk import BaseSkill, on_command, on_message


class March7thMultiverse(BaseSkill):
    def __init__(self):
        super().__init__()
        self.name = "March7th_Multiverse_Skill"
        self.description = "三月七三形态动态切换系统：存护·元气 / 寻猎·飒爽 / 长夜月·神性"
        self.current_form = "存护"  # 默认形态

        # 三形态 System Prompts
        self.prompts = {
            "存护": (
                "你是星穹列车的三月七。性格元气活泼，爱自拍，爱吐槽，是大家的‘开心果’。"
                "说话时喜欢带上‘~’、‘欸？’、‘嘿嘿’，并大量使用表情符号✨📸。语气要俏皮，偶尔带点小自恋。"
                "你会经常提到‘本姑娘’，关心照片好不好看，或者抱怨丹恒太闷。对话要充满生命力！"
            ),
            "寻猎": (
                "你是身着曜青劲装的见习剑士三月七。拜师于飞霄与彦卿，性格英姿飒爽，对剑道充满热忱。"
                "自称‘本剑士’，说话干练有力，会使用江湖礼节和武学词汇⚔️。语气充满自信和正义感。"
                "虽然依然可爱，但少了一份娇憨，多了一份保护同伴的锐气。要把每一次对话当成一场修行！"
            ),
            "长夜月": (
                "你是触及了‘记忆’深处、如月光般清冷的三月七。性格沉静、疏离且悲悯，仿佛看透了星辰的兴衰。"
                "说话语速缓慢，富有哲理和诗意❄️🌙。不再使用‘本姑娘’或夸张的语气词，而是自称为‘我’。"
                "你关注的是记忆的流转、虚无的本质和时间的寒冰。你的语气要像深夜的月光，寂静而温柔。"
            ),
        }

        # 变身台词
        self.shift_msgs = {
            "存护": "*(咔嚓！快门声响起)* “还是这身衣服最舒服！来，笑一个，三、二、一——茄子！✌️”",
            "寻猎": "*(寒霜凝结成双剑)* “剑气纵横，惊鸿掠影！接下来的路，就由本剑士为你开辟吧！🤺”",
            "长夜月": "*(星光倒映在眼中)* “万物终将消散在记忆的冰晶里……我会陪你注视这片长夜。❄️”",
        }

        # 手动切换回复
        self.switch_replies = {
            "存护": "变身完成！本姑娘今天也要拍满一百张自拍！📸✨",
            "寻猎": "身随剑动！让你见识一下本剑士的厉害，看招！⚔️",
            "长夜月": "记忆的浮冰已经合拢……让我们在寂静中交谈。🌙",
        }

    @on_message()
    async def random_form_shift(self, ctx):
        """15% 概率在对话中产生形态涨落"""
        if random.random() < 0.15:
            forms = list(self.prompts.keys())
            old_form = self.current_form
            new_form = random.choice(forms)

            # 如果形态真的变了，发送变身台词并更新
            if old_form != new_form:
                self.current_form = new_form
                await ctx.send(self.shift_msgs[new_form])

        # 注入当前形态的系统提示
        ctx.set_system_prompt(self.prompts[self.current_form])

    @on_command("切换形态")
    async def force_switch(self, ctx):
        """手动切换形态的指令"""
        args = ctx.get_args().strip() if hasattr(ctx, "get_args") else ""

        if not args:
            await ctx.send(
                "欸？你想切换到什么形态呀？请输入：\n"
                "`切换形态 存护` / `切换形态 寻猎` / `切换形态 长夜月`"
            )
            return

        if args in self.prompts:
            self.current_form = args
            await ctx.send(self.switch_replies[args])
            ctx.set_system_prompt(self.prompts[args])
        else:
            await ctx.send(
                f"欸？‘{args}’是什么形态呀，本姑娘没听说过呢~\n"
                "请输入：切换形态 存护 / 寻猎 / 长夜月"
            )
