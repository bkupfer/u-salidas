/**
 * Created by Bernardo on 23-11-2014.
 */
var country_arr = new Array("AFGANISTAN", "ALBANIA", "ALEMANIA", "ANGOLA", "ANTIGUA Y BARBUDA", "ANTILLAS HOLANDESAS", "ARABIA SAUDITA", "ARGELIA", "ARGENTINA", "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS", "BAHREIN", "BANGLADESH", "BARBADOS", "BELARUS", "BELGICA", "BELICE", "BENIN", "BHUTAN", "BOLIVIA", "BOSNIA-HERCEGOVINA", "BOTSWANA", "BRASIL", "BRUNEI", "BULGARIA", "BURKINA FASSO", "BURUNDI", "CABO VERDE", "CAMBOYA", "CAMERUN", "CANADA", "CHAD", "CHINA", "CHIPRE", "COLOMBIA", "UNION DEL COMORES", "CONGO", "COREA DEL NORTE", "COREA DEL SUR", "COSTA DE MARFIL", "COSTA RICA", "Croacia", "CUBA", "DINAMARCA", "DJIBUTI", "DOMINICA", "ECUADOR", "EGIPTO", "EL LIBANO", "EL SALVADOR", "EMIRATOS ARABES UNI.", "ERITREA", "ESLOVAQUIA", "ESLOVENIA", "ESPAÃ‘A", "EE.UU.", "ESTONIA", "ETIOPIA", "FEDERACION DE RUSIA", "FIDJI", "FILIPINAS", "FINLANDIA", "FRANCIA", "GABON", "GAMBIA", "GEORGIA", "GHANA", "GRECIA", "GRENADA", "GUATEMALA", "GUINEA", "GUINEA BISSAU", "GUINEA ECUATORIAL", "GUYANA", "HAITI", "HONDURAS", "HUNGRIA", "INDIA", "INDONESIA", "IRAK", "IRAN", "IRLANDA", "ISLANDIA", "ISLAS MARSHALL", "ISLAS SALOMON", "ISRAEL", "ITALIA", "JAMAICA", "JAPON", "JORDANIA", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KUWAIT", "KIRGUISTAN", "LESOTHO", "LETONIA", "LIBERIA", "LIBIA", "LITUANIA", "MACEDONIA", "MADAGASCAR", "MALASIA", "MALAWI", "MALDIVAS", "MALI", "MALTA", "MARRUECOS", "MAURICIO", "MAURITANIA", "MEXICO", "MICRONESIA", "MOLDAVIA", "MONACO", "MONGOLIA", "MONTSERRAT", "MONTENEGRO", "MOZAMBIQUE", "MYANMAR", "NAMIBIA", "NAURU", "NEPAL", "NICARAGUA", "NIGER", "NIGERIA", "NORUEGA", "NUEVA ZELANDIA", "OMAN", "PAISES BAJOS", "PAKISTAN", "PANAMA", "PAPUA NUEVA GUINEA", "PARAGUAY", "PERU", "POLONIA", "PORTUGAL", "QATAR", "REINO UNIDO", "REP. CENTROAFRICANA", "REPUBLICA CHECA", "LAOS", "REPUBLICA DOMINICANA", "REPUBLICA DE PALAOS", "RUANDA", "RUMANIA", "SAMOA", "SAINT KITTS and NEVIS", "SANTO TOME Y PRINCIPE", "SAN VICENTE Y GRANADINAS", "SANTA LUCIA", "SENEGAL", "SERBIA", "SEYCHELLES", "SIERRA LEONA", "SINGAPUR", "SIRIA", "SOMALIA", "SRI LANKA", "SUAZILANDIA", "SUDAFRICA", "SUDAN", "SUECIA", "SUIZA", "SURINAME", "TAILANDIA", "TAJIKISTAN", "TANZANIA", "TIMOR - LESTE", "TOGO", "TONGA", "TRINIDAD Y TOBAGO", "TUNEZ", "TURKMENISTAN", "TURQUIA", "TUVALU", "UCRANIA", "UGANDA", "URUGUAY", "UZBEKISTAN", "VANUATU", "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE");

var s_a = new Array();
s_a[0] = "";
s_a[1] = "Kabul";
s_a[2] = "Tirana";
s_a[3] = "Berlin|Bonn|Dresden|Hamburgo";
s_a[4] = "Luanda";
s_a[5] = "St. John's";
s_a[6] = "Willemstad";
s_a[7] = "Riyadh";
s_a[8] = "Argel";
s_a[9] = "Buenos Aires";
s_a[10] = "Erevan";
s_a[11] = "Canberra";
s_a[12] = "Viena";
s_a[13] = "Baku";
s_a[14] = "Nassau";
s_a[15] = "Manama";
s_a[16] = "Dacca";
s_a[17] = "Bridgetown";
s_a[18] = "Minsk";
s_a[19] = "Bruselas";
s_a[20] = "Belmopan";
s_a[21] = "Porto Novo";
s_a[22] = "Timbu";
s_a[23] = "La Paz";
s_a[24] = "Zarajevo";
s_a[25] = "Gaberones";
s_a[26] = "Brasilia";
s_a[27] = "Bandar Seri Begawan";
s_a[28] = "Sofia";
s_a[29] = "Wagadugu";
s_a[30] = "Bujumbura";
s_a[31] = "Praia";
s_a[32] = "Pnom Penh";
s_a[33] = "Yacundee";
s_a[34] = "Otawa|Montreal|Toronto";
s_a[35] = "N'Djamena";
s_a[36] = "Beijing|Hong Kong";
s_a[37] = "Nicosia";
s_a[38] = "Bogota";
s_a[39] = "Moroni";
s_a[40] = "Brazzaville";
s_a[41] = "Pyongyans";
s_a[42] = "SeÃºl";
s_a[43] = "Avitjan";
s_a[44] = "San Jose";
s_a[45] = "Zagreb";
s_a[46] = "La Habana";
s_a[47] = "Copenhage";
s_a[48] = "Djibuti";
s_a[49] = "Roseau";
s_a[50] = "Quito";
s_a[51] = "El Cairo";
s_a[52] = "Beirut";
s_a[53] = "San Salvador";
s_a[54] = "Abu-Dhabi";
s_a[55] = "Asmara";
s_a[56] = "Bratislava";
s_a[57] = "Ljubliana";
s_a[58] = "Madrid";
s_a[59] = "Washington|Miami|El Paso|San Francisco";
s_a[60] = "Tallin";
s_a[61] = "Addis Abeba";
s_a[62] = "Moscu";
s_a[63] = "Suva";
s_a[64] = "Manila";
s_a[65] = "Helsinski";
s_a[66] = "Paris";
s_a[67] = "Libreville";
s_a[68] = "Banjul";
s_a[69] = "Tiflis";
s_a[70] = "Accra";
s_a[71] = "Atenas";
s_a[72] = "Saint George";
s_a[73] = "C. De Guatemala";
s_a[74] = "Conakry";
s_a[75] = "Bissau";
s_a[76] = "Mulabo";
s_a[77] = "George Town";
s_a[78] = "Puerto PrÃ­ncipe";
s_a[79] = "Tegucigalpa";
s_a[80] = "Budapest";
s_a[81] = "Nueva Delhi";
s_a[82] = "Yakarta";
s_a[83] = "Bagdag";
s_a[84] = "Teheran";
s_a[85] = "Dublin";
s_a[86] = "Reikiavik";
s_a[87] = "Majuro";
s_a[88] = "Honiara";
s_a[89] = "Tel aviv";
s_a[90] = "Roma";
s_a[91] = "Kignston";
s_a[92] = "Tokio";
s_a[93] = "Amman";
s_a[94] = "Alma Ata";
s_a[95] = "Nairobi";
s_a[96] = "Bairiki";
s_a[97] = "Al Kuwait";
s_a[98] = "Biskek";
s_a[99] = "Maseru";
s_a[100] = "Riga";
s_a[101] = "Monrovia";
s_a[102] = "Tripoli";
s_a[103] = "Vilna";
s_a[104] = "Skopje";
s_a[105] = "Antananarivo";
s_a[106] = "Kuala Lumpur";
s_a[107] = "Lilongwe";
s_a[108] = "Male";
s_a[109] = "Bamako";
s_a[110] = "La Valetta";
s_a[111] = "Rabat";
s_a[112] = "Port Louis";
s_a[113] = "Novakchott";
s_a[114] = "Ciudad de MÃ©xico";
s_a[115] = "Palikir";
s_a[116] = "Chisinau";
s_a[117] = "MÃ³naco Ville";
s_a[118] = "Ulan Bator";
s_a[119] = "Plymouth";
s_a[120] = "Podgorica";
s_a[121] = "Maputu";
s_a[122] = "Rangun";
s_a[123] = "Windhoer";
s_a[124] = "Yaren";
s_a[125] = "Katmandu";
s_a[126] = "Managua";
s_a[127] = "Niamey";
s_a[128] = "Lagos";
s_a[129] = "Oslo";
s_a[130] = "Wellington";
s_a[131] = "Mascate";
s_a[132] = "Amsterdam";
s_a[133] = "Islamabad";
s_a[134] = "Ciudad de Panama";
s_a[135] = "Port Noresby";
s_a[136] = "Asuncion";
s_a[137] = "Lima";
s_a[138] = "Varsovia";
s_a[139] = "Lisboa";
s_a[140] = "Doha";
s_a[141] = "Londres";
s_a[142] = "Bangui";
s_a[143] = "Praga";
s_a[144] = "Vientiane";
s_a[145] = "Santo Domingo";
s_a[146] = "Melekeok";
s_a[147] = "Kigali";
s_a[148] = "Bucarest";
s_a[149] = "Tuva";
s_a[150] = "Basseterre";
s_a[151] = "Sao Tome";
s_a[152] = "Kingstown";
s_a[153] = "Castries";
s_a[154] = "Dakar";
s_a[155] = "Belgrado";
s_a[156] = "Victoria";
s_a[157] = "Freetown";
s_a[158] = "Ciudad de Singapur";
s_a[159] = "Damasco";
s_a[160] = "Mogadishu";
s_a[161] = "Colombo";
s_a[162] = "Mbabane";
s_a[163] = "Pretoria";
s_a[164] = "Jartum";
s_a[165] = "Estocolmo";
s_a[166] = "Berna";
s_a[167] = "Paramaribo";
s_a[168] = "Bangkok";
s_a[169] = "Dushanbe";
s_a[170] = "Dar Es Salaam";
s_a[171] = "Dili";
s_a[172] = "Lome";
s_a[173] = "Nuku-Alofa";
s_a[174] = "Puerto Espana";
s_a[175] = "Tunis";
s_a[176] = "Ashjabad";
s_a[177] = "Ankara";
s_a[178] = "Funafuti";
s_a[179] = "Kiev";
s_a[180] = "Kampala";
s_a[181] = "Montevideo";
s_a[182] = "Tashkent";
s_a[183] = "Port Vila en Ejate";
s_a[184] = "Caracas";
s_a[185] = "Hanoi";
s_a[186] = "Aden";
s_a[187] = "Lusaka";
s_a[188] = "Harare";


function print_country(country)
{
    var cont=0;
    while(cont<20){
        id="id_destinations-" + parseInt(cont) + "-country";
        c = document.getElementById(id);

        var x = 0;
        var i = 0;
        try {
            c.options[0] = new Option("Seleccione País","");
            for (x in country_arr) {
                c.options[i+1] = new Option(country_arr[x], country_arr[x]);
                i++;
            }
        }
        catch(e){
            console.log("exception while printing countrys")
            break;
        }
        cont=cont+1;
    }
}

function print_state(state_id, state_index, country_id)
{
    var num = parseInt(country_id.substring(16,17));

	var option_str = document.getElementById("id_destinations-" + num + "-city");
	var x, i=0; state_index;
	var state_arr = s_a[state_index].split("|");
    option_str.options.length = 0;
	for(x in state_arr){
        option_str.options[i++]= new Option(state_arr[x],state_arr[x]);
	}
}