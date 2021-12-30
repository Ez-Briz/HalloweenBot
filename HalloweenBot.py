import discord
from discord import file
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import io
import aiohttp
import random
import asyncio


client = commands.Bot(command_prefix="!", help_command = None)
slash = SlashCommand(client, sync_commands=True)
available = True
isBotActive = False
########################################################################################################################
########################################################################################################################
############################################\\\\\\\\\VARIABLES/////////#################################################
########################################################################################################################
########################################################################################################################
timeToWait = 3
callAdminMessage = "У Вас нет доступа. Обратитесь к создателю бота -> https://vk.com/eznekit"
notActiveMessage = "Бот неактивен. Попробуйте позже."
waitMessage = "Подождите " + str(timeToWait) + " секунды, прежде чем попробовать снова!"
errorMessage = "Ошибка! Обратитесь к модераторам."
noAvailableMessage = "Больше нет доступных ролей."
currentStatusMessage = "Состояние бота изменено."
alreadyHaveMessage = "Вы уже выбрали себе роль!"
reloadMessage = "Список ролей перезаписан, роли сброшены!"
pers = {"**Майкл Майерс | Michael Myers**" : [
            "> Вы — маньяк-убийца и психопат, одержимый духом Самайна. Ваше любимое оружие — это  большой столовый нож. Вы тихо следите за своей жертвой и выжидаете идеальный момент, чтобы убить. Вы накаляете атмосферу своей слежкой и доводите жертву до паники.",
            "https://cubiq.ru/wp-content/uploads/2017/10/dbdshdw.jpg"
            ],
        "**Джейсон Вурхиз | Jason Voorhees**" : [
            "> Вы — серийный убийца в хоккейной маске. Вашим оружием является мачете. Вы мертвец, который вдруг ожил в пятницу 13го и отправлялись убивать любого, кто оказывался рядом с озером. Вы крайне жестоко убиваете своих жертв различными способами.",
            "https://topspiski.com/wp-content/uploads/2017/11/djeison-700x457.jpg"
            ],
        "**Фредди Крюгер | Freddy Krueger**" : [
            "> Вы — маньяк-убийца. Ваше оружие — перачатка, которую вы носите на правой руке с острыми металлическими лезвиями на кончиках пальцев. Вы можете убивать людей в их же снах, но иногда прорываетесь и в реальный мир, где продолжаете наводить страх и ужас.",
            "https://datainfox.com/wp-content/uploads/2019/11/freddy-krueger-35t.jpg"
            ],
        "**Бубба Сойер | Bubba Sawyer**" : [
            "> Вы — психопат и каннибал. Ваша маска сделана из кожи ваших жертв. Ваше поведение часто напоминает поведение маленького ребёнка, не до конца понимающего, что он делает. В качестве оружия Вы используете различные предметы — молоток, нож, топор, крюк для мяса — но чаще всего при Вас бензопила, при помощи которой Вы избавляетесь от своих жертв.",
			"https://bloodyflicksblog.files.wordpress.com/2021/03/texas-chainsaw.jpg"
            ],
        "**Джипперс Криперс | Jeepers Creepers**" : [
            "> Вы — человекоподобный монстр, который в течение 23 дней каждую 23 весну убивает и поедает человеческие органы с целью продления своего существования, а также с целью регенерации. Вы выбираете нужных доноров по запаху. Через человеческий страх Вы получаете всю информацию о состоянии здоровья жертвы.",
			"https://www.nonapritequestoblog.it/wp-content/uploads/2017/11/Jeepers-Creepers-4.jpg"
            ],
        "**Конструктор | Jigsaw**" : [
            "> Вы — гениальный маньяк, но Вы не считаете себя убийцей. Ваше настоящее имя Джон Крамер. Вы расставляете для жертв опасные ловушки, пройдя которые можно остаться в живых. Однако для этого несчастным приходится подвергать себя тяжелым физическим увечьям. В этом заключается Ваша концепция — Вы считаете, что таким образом открываете людям то, насколько ценна их жизнь и как следует платить за свои ужаснейшие ошибки.",
			"https://media.distractify.com/brand-img/ygQrWzP3h/0x0/jigsaw-saw-movie-1580923819634.jpg"
            ],
        "**Немезис | Nemesis**" : [
            "> Вы — экспериментальный образец, который был создан корпорацией Umbrella. Ваша цель — уничтожение отряда S.T.A.R.S. Вы обладаете дюжиной силой и способны одним взмахом сносить все препятствия на своём пути.",
			"https://avatars.mds.yandex.net/get-zen_doc/1875939/pub_5e8a9b9e9858d7030b84605b_5e8aa120e4ab702789ae6824/scale_2400"
            ],
        "**Тиран | Tyrant**" : [
            "> Вы — биоорганическое оружие и непосредственная собственность корпорации Umbrella. Вы были созданы для убийств неугодных и тех, кто много знает. Не смотря на Ваше происхождение, Ваш интеллект примерно равен интеллекту человека. Вы экипированы пуленепробиваемым плащом и собственными мышцами, которые помогают вам исполнить любой приказ.",
			"https://piterplay.com/image/catalog/resident-evil-2-mr-x-article2.png"
            ],
        "**Свинья | The Pig**" : [
            "> Вы — убийца, верный помощник и преемник Конструктора. Ваше настоящее имя — Аманда Янг. Поскольку Вы помогали во многом Джону Крамеру, то научились скрытно передвигаться преследуя будущую жертву, а затем резко нападаете на неё. Вы навечно преданны делу своего учителя, наказываете неблагодарных и виновных с помощью своей хитрости и убийственных ловушек.",
			"https://mocah.org/uploads/posts/344286-Dead-by-Daylight-Video-Game-The-Pig-Amanda-Young-Saw.jpg"
            ],
        "**Пирамидаголовый | Pyramid Head**" : [
            "> Вы — ужасающий монстр, проявление вины Джеймса Саливана и его желания быть убитым. У Вас на голове огромная железная пирамида, которая вгоняет людей в ужас. Вы повсюду таскаете свой огромный Великий нож, которым Вы и вершите правосудие. Вас называют палачом, а каждый житель Сайлент Хилла бежит в ужасе, когда слышит скрежет вашего меча.",
			"https://cdn.igromania.ru/mnt/news/c/d/a/1/b/5/94616/16940d15baa3c8b1_1920xH.jpg"
            ],
        "**Медсестра | Nurse**" : [
            "> Некогда Вас считали человеком. Желание помочь несчастной сгоревшей девочке - Алессе Гиллеспи привело к тому, что Вы стали одним из самых страшных ужасов Сайлент Хилла. Вооружившись ножом, Вы убиваете всех, кого способны заметить. Никому не скрыться от Вас, пока горит свет.",
			"https://cdn.wallpapersafari.com/75/3/5ytJPE.jpg"
            ],
        "**Слендермен | Slenderman**" : [
            "> Вы — мистическое ужасающее существо. Вы примерно 2 метра ростом, молча стоите в тумане или за стеной дождя и наблюдаете своей безликой физиономией за будущими жертвами. Поговаривают, что Вы обладаете телепатией, дабы вселять ещё больший ужас и панику в сердца людей.",
			"https://politpuzzle.ru/wp-content/uploads/2017/04/31088-slender2-750x422.jpg"
            ],
        "**Граф Дракула |  Count Dracula**" : [
            "> Вы — могущественный вампир. Ваш источник жизненный силы — это кровь. Она делает Вас крепче, сильнее и даже возвращает Ваше увядающие за многие века молодость. В то время как долгое отсутствие крови в Вашем рационе заметно старит и иссушает. За многие века Вы изучили очень много книг, однако, каким бы умным и сильным вампиром Вы не были, при виде крови, Вы словно теряете рассудок и готовы иссушить тело своей жертвы, не оставляя даже и капли.",
			"https://avatars.mds.yandex.net/get-kinopoisk-post-img/1101236/08b2ee8e015dd4e7f3425230addf5e7c/960x540"
            ],
        "**Пеннивайз | Pennywise**" : [
            "> Вы — монстр (оборотень, перевёртыш), который использует облик клоуна, ведь так легче приманивать детей. Вы используете страх как приправу, поскольку мясо полумертвых от ужаса жертв гораздо вкуснее. Вы не лишены извращенного чувства юмора и творческой жилки, ведь с явным удовольствием мучаете своих жертв и играете с ними. Себя Вы очень восхваляете и называете \"Пожирателем миров\".",
			"https://www.b17.ru/foto/uploaded/upl_1518809627_21061.jpg"
            ],
        "**Пинхед | Pinhead**" : [
            "> Вы — сенобит, существо, обитающее в ином измерении, наслаждающиеся насилием, жестокими убийствами. Вы способны на расстоянии управлять цепями с прикреплёнными к ним крючьями. Хоть Вы и возглавляете сенобитов, но не лишены понимания справедливости и остатков человеческих чувств.",
			"https://newizv.ru/attachments/7d9056e8aa45f04a655e4f22278e2a3b784ebea5/store/limit/700/393/95/ac1a91b88bb7bdcd7d144e69a904c019383cbe050e13c0a936b13860caa9/5e1d3e339fdd1.jpeg"
            ],
        "**Чаки | Chucky**" : [
            "> Вы — кукла-убийца. Вашим прозвищем при жизни было \"Чикагский душитель\". Если Вы  появлялись в семье, начинались несчастья. В доме словно селился дьявол, избавиться от которого было невозможно. Владельцы такой куклы исчезали или заканчивали жизнь в психиатрической больнице, впав в безумство.",
			"https://www.belta.by/images/storage/news/with_archive/2018/000029_1530885469_309465_big.jpg"
            ],
        "**Нечто | Thing**" : [
            "> Вы — инопланетная форма жизни. Ваша главная цель - порабощение всего живого и ассимилирование всех и каждого на своём пути. Вы нападаете из засады и убиваете свою жертву. После успешного убийства, вы можете принять облик своей жертвы и успешно подражать ей.",
			"https://toposrednik.ru/wp-content/uploads/2021/04/big_58427_the-thing_e88a14-1024x697.jpg"
            ],
        "**Чужой | Alien**" : [
            "> Вы — идеальный организм: Вас сложно убить и, даже будучи раненным или погибая, Вы способны причинить вред, так как в Вашей крови содержится сильнейшая кислота. Вы лишены развитого интеллекта, но имеете мощные инстинкты, направленные прежде всего на выживание. Ваш животный инстинкт подсказывает Вам, что люди — это всего-лишь Ваша пища. С помощью своих двойных челюстей и острых когтей, Вы с лёгкостью терзаете плоть жертвы отрывая кусок за куском.",
			"https://www.soyuz.ru/public/uploads/files/2/7445979/202009071247044ea5a7c3a9.jpg"
            ],
        "**Демогоргон | Demogorgon**" : [
            "> Вы — хищное человекоподобное существо, прибывшее в этот мир из параллельного измерения называемого Изнанкой. У вас хорошо развито обоняние, благодаря чему Вы и выслеживаете своих жертв. Своими длинными когтями Вы впиваетесь в тело жертвы истерзывая его на куски, а после пожираете своей раскрывающейся, как цветок пастью.",
			"https://apjournal.ru/wp-content/uploads/2019/10/2019-10-31_13-02-06.png"
            ],
        "**Джокер | Joker**" : [
            "> Вы — безумный психопат, маньяк и Вас действительно можно назвать суперзлодеем. Несмотря на Ваше очевидное безумство, Вы обладаете довольно высоким коэффициентом интеллекта, хитростью и изобретательностью. Те, кто считают Вас союзником, как правило, просто используются Вами. А те, кто нанимают Вас для «грязной работы», должны быть готовы к непредсказуемым результатам. Ваш безумный мозг всегда подсказывает  неожиданные, остроумные и верные решения. Вам нет равных в умении находить слабые места своих противников и использовать против них их же оружие.",
			"https://giknutye.ru/wp-content/uploads/2016/08/joker-istoriya.jpg"
            ],
        "**Бледный человек | Pale man**" : [
            "> При жизни, Вы были слепым стариком, которого вечно били и Вы никак не могли ответить. Но однажды Ваши обидчики переборщили и Вы умерли. И тогда, в аду, Дъявол дал Вам глаза, которые установил на Ваши ладони и отправил отомстить обидчикам. После свершённой мести, Вы стали бродить по деревням и убивать воров. В этом Вам помогают Ваши чёрный и острые когти.",
			"http://pm1.narvii.com/6824/dbb40e28a5fb214e5ec63026ac3bf01aef016790v2_00.jpg"
            ],
        "**Ганнибал Лектер | Hannibal Lecter**" : [
            "> Вы — очень образованный, культурно и интеллектуально развитый психиатр и хирург, одновременно серийный убийца, который практикует на своих жертвах каннибализм. Ваш принцип заключается в том, чтобы «поглотить уродство», которое портит этот мир.",
			"https://avatars.mds.yandex.net/get-kinopoisk-post-img/1101693/e0255ec7113018593b7cbd244894916c/960x540"
            ],
        "**Они | Oni**" : [
            "> Некогда Вы были известны под именем Казан Ямаока. Вы были самураем и Вам было мало просто поддерживать честь своего рода. Вы стремились к большему. Вы хотели властвовать во всей Японии. Но погибнув, Вы так и не смогли осуществить свою мечту до конца. Это не давало покоя Вашей душе и Вы стали жаждущим крови демоном. Ваша верная катана и тяжёлый самурайский доспех - Ваши самые верные напарники. А те, кто смог избежать этой участи будут раздавлены под ударами огромной дубины.",
			"https://sun9-23.userapi.com/impg/c854520/v854520796/21ea3d/Z9XRrva4Bes.jpg?size=604x340&quality=96&sign=d9630f49f1d7ea9844b46c24f36cf77d&type=album"
            ],
        "**Крик | Ghost Face**" : [
            "> Вы — Дэнни Джонсон. Жуткий убийца, способный благодаря своей силе \"Ночной саван\" выслеживать и бесшумно подкрадываться к своим жертвам. Попавшие под воздействие силы Выжившие окажутся уязвимы и не будут знать о присутствии убийцы. Им придётся использовать свои органы чувств, чтобы защититься от него.",
			"https://sun9-5.userapi.com/impf/c855428/v855428130/1691e5/BkngU2oLCL4.jpg?size=510x340&quality=96&crop=150,0,1620,1080&sign=a87585f0e8c3b81bafd778271e27c227&type=album"
            ],
        "**Джек Скеллингтон | Jack Skellington**" : [
            "> Вы — высокий и одетый в чёрный фрак скелет. Вы являетесь душой и самой знаменитой личностью в городе \"Хеллоуин\". Каждый его житель доверяет Вам и способен обратиться за помощью в случае чего. Вы невероятно ловкий и харизматичный скелет. Вы влюблены в девушку-куклу по имени Салли.",
			"https://99px.ru/sstorage/53/2015/10/tmb_146647_7328.jpg"
            ],
        "**Салли Фейс | Sally Face**" : [
            "> Вы — парень подросткового возраста. Из-за одного случая Вы очень пострадали и поэтому на Вашем лице теперь протез. Вы поселились в доме с отцом, где познакомились с некоторыми людьми и нашли замечательного лучшего друга Ларри. В доме происходили таинственные и непонятные ситуации, однако Вы хладнокровно встречались с ними лицом к лицу.",
			"https://otzomir.com/wp-content/uploads/2018/12/_3465_1.png"
            ],
        "**Банши | Banshee**" : [
            "> Вы — девушка, которая, является возле дома обречённого на смерть человека и своими характерными стонами и рыданиями оповещает, что час его кончины близок. На самом деле, Вы способны принимать различные облики: от страшной старухи до бледной красавицы.",
			"https://static.wikia.nocookie.net/mythological-creation/images/2/2b/%D0%91%D0%B0%D0%BD%D1%88%D0%B8.jpg/revision/latest?cb=20161001055729&path-prefix=ru"
            ],
        "**Эмили | Emily**" : [
            "> Вы — невеста из мира мёртвых. Вы привлекательная и, несмотря на то, что была убита, нежная, ранимая, обаятельная девушка. Вы были обмануты, ограблены и убиты ужасным лордом Баркисом, после чего дали себе клятву, что не будете свободны до тех пор, пока не встретите настоящую любовь.",
			"https://img3.goodfon.ru/wallpaper/nbig/7/67/corpse-bride-trup-nevesty.jpg"
            ],
        "**Оборотень | Werewolf**" : [
            "> Вы — мифологическое существо, обладающее способностью превращаться из человека в животное или наоборот. Ваши сверхъестественные силы растут с приближением полнолуния. Вы обладаете самыми различными способностями, такими как: сверхчеловеческая сила, ловкость, скорость и рефлексы, обострённые чувства и так далее. Вашей главной слабостью является аконит.",
			"https://azerhistory.com/wp-content/uploads/2017/09/oboroten-werewolf-1.jpg"
            ],
        "**Зомби | Zombie**" : [
            "> Вы — мертвец, который восстал. Вы не осознаёте себя. Грубо говоря, Вы — кусок мяса, движимый лишь одним инстинктом — есть. Вы способны заразить человека вирусом. Однако Вы видите, чувствуете запах и слышите. Ваше слабое место — мозг. *\"Эти твари еле ходят. Не давай им дотронуться до тебя. Один укус и все кончится.\"*",
			"https://i.pinimg.com/originals/51/aa/f2/51aaf2e49546ded11c7fcd75b236e19e.jpg"
            ],
        "**Ван Хельсинг | Van Helsing**" : [
            "> Вы — известный охотник на вампиров. Ещё с детства Вас считали левой рукой Господа и обучали убийству нечисти. Вы постоянно таскаете с собой многозарядный арбалет, святую воду и распятие Христа, которое помогает вам бороться с нечистой силой.",
			"https://images3.alphacoders.com/181/181885.jpg"
            ],
        "**Самара Морган | Samara Morgan**" : [
            "> Вы — призрак в белом платье и с длинными чёрными волосами, закрывающими лицо. Вы имеете способность убивать людей одним лишь взглядом. Причём причину смерти установить не удается, создаётся впечатление, что у жертвы просто остановилось сердце. У умершего перекошенное от ужаса лицо.",
			"https://www.film.ru/sites/default/files/styles/epsa_1024x450/public/27537513-935425.jpg"
            ],
        "**Ведьма | Witch**" : [
            "> Вы - женщина, практикующая магию (колдовство), а также обладающая магическими способностями и знаниями. Училась ведьма у другой ведьмы или даже у самого чёрта. Народные пересказы связывают с процессом «инициации» ведьмы ритуалы, такие как, например, топтание иконы, прочтение молитвы наоборот, перебрасыванием через нож. Старшая ведьма также может умывать свою ученицу волшебным отваром, после чего та вылетала на улицу через печь и возвращалась уже ведьмой.",
			"https://img4.goodfon.ru/wallpaper/nbig/1/a6/anime-art-akademiia-vedmochek-little-witch-academia-vedma-de.jpg"
            ],
        "**Франкенштейн | Frankenstein**" : [
            "> Вы — создание Виктора Франкенштейна, который хотел создать живое существо из неживой материи. В результате у него получилось создать существо, но ваш вид повергает в ужас даже самого доктора. Вы лишены сознания и совершаете яростные убийства чисто инстинктивно, не осознавая происходящего. Ваш самый большой страх — огонь.",
			"https://www.bestiary.us/files/images/frankenstein1.jpg"
            ],
        "**Ктулху | Cthulhu**" : [
            "> Вы — божество, Зверь миров, спящий на дне Тихого океана, но, тем не менее, способный воздействовать на разум человека. Вы лежите окутанные сном, подобному смерти, на вершине подводного города Р’льех посреди Тихого океана. «При верном положении звёзд» Р’льех появляется над водой, и Вы освобождаетесь. В «Зове Ктулху» сны, напускаемые Вами, сильно ужасают видевших их, и порой доводят до сумасшествия.",
			"https://vgtimes.ru/uploads/posts/2019-05/1558358192_2.-paint.jpg"
            ],
        "**Призрак | Ghost**" : [
            "> Вы — душа умершего человека, которая стала видимой в реальной жизни. Вы можете быть привязаны к определённому месту или же к какому-либо человеку, следуя за ним и наблюдая. Если сильно постараться, то Вы иногда можете перемещать предметы. Поскольку Вы паранормальное явление, то люди испытывают страх перед Вами и могут даже сойти с ума.",
			"https://img5.goodfon.ru/wallpaper/nbig/f/f9/prizraki-prokliatoe-mesto-tuman-v-lesu-noch-dukhi-prividenii.jpg"
            ],
        "**Харли Квинн | Harley Quinn**" : [
            "> Вы — сумасбродная суперзлодейка и противница Бэтмена, наиболее известная как девушка и напарница Джокера, с недавних пор начавшая выстраивать одиночную криминальную карьеру. Будучи в прошлом психиатром лечебницы Аркхем, Вы лично занималась лечением Джокера, пока не влюбились в безумного убийцу.",
			"https://images.glavred.info/2020_01/thumb_files/600x420/1580056973-4925.jpg"
            ],
        "**Фредди | Freddy**" : [
            "> Вы — аниматроник-медведь, который находится в режиме «cвободного роуминга» как и другие аниматроники. Имеет длинные и массивные конечности, которые скреплены стальными суставами эндоскелета. Фредди является восстановленным аналогом своей Сломанной версии, которую отреставрировали и стали использовать после того, как аниматроники Игрушечной линейки были отправлены на утилизацию в связи с неисправностью. Фредди с 1985 года одержим духом мальчика Габриэля, которого Уильям Афтон вместе с остальными 3 детьми убил в первой «Пиццерии Фредди Фазбера».",
			"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpfD7FOVJ4oAabxc3CjrIjNODcaNJWhd3Asg&usqp=CAU"
            ],
        "**Смерть | Death**" : [
            "> Вы — само воплощение угасания жизни и её конца. Вас представляют в образе загадочной личности, что скрывает свой лик за чёрным капюшоном. Вы провожаете усопших в мир иной и приходите за ещё живыми. Ваша коса, служит инструментом для того, чтобы обрезать линию жизни связывающих выживших с миром людей.",
			"https://cs8.pikabu.ru/post_img/big/2016/07/08/6/1467966462129264624.jpg"
            ],
        "**Кровавая Мэри | Bloody Mary**" : [
            "> Вы — ужасающий дух девушки. Вас призывают подростки возле зеркала, произнося Ваше имя несколько раз. После этого Вы появляетесь и утаскиваете за собой шутников, жестоко убивая.",
			"http://xn--e1aahgrctjf9g.com/wp-content/uploads/2018/12/istoriya-krovavoj-mehri1-1024x500.jpg"
            ],
        "**Пиковая дама | Queen of spades**" : [
            "> Вы — дух женщины, которого частенько любят призывать детишки ради веселья. Произнеся три раза: \"Пиковая дама, приди к нам\", Вы появляетесь и приносите хаос. Вы отождествляетесь, как приносящая неудачи, также Вас сравнивают с ведьмой. Поговаривают, что Вы можете даже забрать свою жертву в мир зазеркалья и там жестоко расправиться с ней.",
			"https://www.film.ru/sites/default/files/filefield_paths/the_queen_of_spades.jpg"
            ],
        "**Краснолиций демон | Lipstick-Face Demon**" : [
            "> Вы — демон обитающий в уголке места называемого Астралом. Вы напоминаете беса, с красным лицом, хвостом, ножками как у сатира и очень острыми когтями, которые вы изрядно любите затачивать под музыку. Ранее вы были маньяком работающим в кукольном театре. Вашими жертвами зачастую были дети и их родители.",
			"https://shhjokino.mir-kvestov.ru/uploads/quests/4748/large/1.jpg?1504056176"
            ],
        "**Дюллахан | Dyullahan**" : [
            "> Вы – Дулахан, злобный дух, представляющий собой чудовищного безголового всадника, как правило, на чёрном коне, несущий свою голову в руках. В качестве кнута дуллахан пользуется человеческим позвоночником. Когда дуллахан останавливает своего коня, это означает, что кого-то ждёт смерть. От дуллахана нельзя защититься. Дуллахан очень боится золота, и даже небольшого прикосновения к нему этим металлом достаточно, чтобы прогнать его.",
			"https://monbook.ru/sites/default/files/dullahan.jpg"
            ]
        }
persSave = dict(pers)
userPerson = {}
########################################################################################################################

@slash.slash(
    name = "Start", # Command name
    description= "Start or stop bot", # Description for current command
    guild_ids=[721836486751944754, 718885084199125114] # Channel ID (right click to channel -> copy ID (with developer mod in discord settings))
)
async def _start(ctx:SlashContext):
    global pers, userPerson, isBotActive, persSave
    if not isAdmin(ctx):
        await ctx.send(callAdminMessage)
        return
    isBotActive = not isBotActive
    await ctx.send(currentStatusMessage + ' Текущий статус: ' + ('**Запущен**' if isBotActive else '**Отключён**'))

@slash.slash(
    name = "Reload", # Command name
    description= "Reload current halloween list", # Description for current command
    guild_ids=[721836486751944754, 718885084199125114] # Channel ID (right click to channel -> copy ID (with developer mod in discord settings))
)
async def _reload(ctx:SlashContext):
    global persSave, pers, userPerson
    if not isBotActive:
        await ctx.send(notActiveMessage)
        return
    if not isAdmin(ctx):
        await ctx.send(callAdminMessage)
        return
    pers = dict(persSave)
    userPerson.clear()
    await ctx.send(reloadMessage)

@slash.slash(
    name = "HRole", # Command name
    description= "Gives you random role from a pool", # Description for current command
    guild_ids=[721836486751944754, 718885084199125114] # Channel ID (right click to channel -> copy ID (with developer mod in discord settings))
)
async def _hrole(ctx:SlashContext):
    if not isBotActive:
        await ctx.send(notActiveMessage)
        return
    global available
    if (available):
        available = not available
        asyncio.create_task(ChangeState())
    else:
        await ctx.send(waitMessage) 
        return
    role = {}
    if (ctx.author.id in userPerson):
        await ctx.send(alreadyHaveMessage)
        await PrintAllInfo(userPerson[ctx.author.id], ctx)
        return
    elif len(pers) > 0:
        role = random.choice(list(pers.keys()))
        pers.pop(role)
        userPerson[ctx.author.id] = role
    else:
        await ctx.send(noAvailableMessage)
        return
    await PrintAllInfo(role, ctx)
            

async def ChangeState():
    global available
    await asyncio.sleep(timeToWait)
    available = not available

async def PrintAllInfo(role, ctx:SlashContext):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(persSave[role][1], allow_redirects=True) as resp:
                data = io.BytesIO(await resp.read())
                await ctx.send(role + "\n" + persSave[role][0] + "\n", file=discord.File(data, 'image.png')) # Response
                
    except Exception as exp:
        await ctx.send(errorMessage)
        print('=======ERROR=======')
        print(exp)
        print(type(exp))
        print('===================')

def isAdmin(ctx:SlashContext):
    id = str(ctx.author.id)
    if id == '264770311646478341' or id == '358630498207137802' or id == '405878763835097088':
        return True
    else:
        return False



@client.event
async def on_ready():
    print(f"Bot have logged in as {client.user}")


client.run("ODk4NTQ2ODgxNDEwNDk4NTg5.YWly_g.kjArGrZn5iSW7hWavd2ZLhmf5P0")
