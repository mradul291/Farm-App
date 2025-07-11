// Copyright (c) 2025, chirag and contributors
// For license information, please see license.txt

frappe.ui.form.on("Site", {
    state: function (frm) {
        let state = frm.doc.state; // Get selected state
        let lgaList = {
            Abia: [
                "Aba North", "Aba South", "Arochukwu", "Bende", "Ikwuano",
                "Isiala Ngwa North", "Isiala Ngwa South", "Isuikwuato",
                "Obi Ngwa", "Ohafia", "Osisioma", "Ugwunagbo", "Ukwa East",
                "Ukwa West", "Umuahia North", "Umuahia South", "Umu Nneochi"
            ],
            Adamawa: [
                "Demsa", "Fufure", "Ganye", "Gayuk", "Gombi", "Grie", "Hong",
                "Jada", "Larmurde", "Madagali", "Maiha", "Mayo Belwa", "Michika",
                "Mubi North", "Mubi South", "Numan", "Shelleng", "Song",
                "Toungo", "Yola North", "Yola South"
            ],
            AkwaIbom: [
                "Abak",
                "Eastern Obolo",
                "Eket",
                "Esit Eket",
                "Essien Udim",
                "Etim Ekpo",
                "Etinan",
                "Ibeno",
                "Ibesikpo Asutan",
                "Ibiono-Ibom",
                "Ika",
                "Ikono",
                "Ikot Abasi",
                "Ikot Ekpene",
                "Ini",
                "Itu",
                "Mbo",
                "Mkpat-Enin",
                "Nsit-Atai",
                "Nsit-Ibom",
                "Nsit-Ubium",
                "Obot Akara",
                "Okobo",
                "Onna",
                "Oron",
                "Oruk Anam",
                "Udung-Uko",
                "Ukanafun",
                "Uruan",
                "Urue-Offong Oruko",
                "Uyo"
            ],
            
            Anambra: [
                "Aguata",
                "Anambra East",
                "Anambra West",
                "Anaocha",
                "Awka North",
                "Awka South",
                "Ayamelum",
                "Dunukofia",
                "Ekwusigo",
                "Idemili North",
                "Idemili South",
                "Ihiala",
                "Njikoka",
                "Nnewi North",
                "Nnewi South",
                "Ogbaru",
                "Onitsha North",
                "Onitsha South",
                "Orumba North",
                "Orumba South",
                "Oyi"
            ],
            Bauchi: [
                "Alkaleri",
                "Bauchi",
                "Bogoro",
                "Damban",
                "Darazo",
                "Dass",
                "Gamawa",
                "Ganjuwa",
                "Giade",
                "Itas-Gadau",
                "Jama are",
                "Katagum",
                "Kirfi",
                "Misau",
                "Ningi",
                "Shira",
                "Tafawa Balewa",
                " Toro",
                " Warji",
                " Zaki"
            ],

            Bayelsa: [
                "Brass",
                "Ekeremor",
                "Kolokuma Opokuma",
                "Nembe",
                "Ogbia",
                "Sagbama",
                "Southern Ijaw",
                "Yenagoa"
            ],
            Benue: [
                "Agatu",
                "Apa",
                "Ado",
                "Buruku",
                "Gboko",
                "Guma",
                "Gwer East",
                "Gwer West",
                "Katsina-Ala",
                "Konshisha",
                "Kwande",
                "Logo",
                "Makurdi",
                "Obi",
                "Ogbadibo",
                "Ohimini",
                "Oju",
                "Okpokwu",
                "Oturkpo",
                "Tarka",
                "Ukum",
                "Ushongo",
                "Vandeikya"
            ],
            Borno: [
                "Abadam",
                "Askira-Uba",
                "Bama",
                "Bayo",
                "Biu",
                "Chibok",
                "Damboa",
                "Dikwa",
                "Gubio",
                "Guzamala",
                "Gwoza",
                "Hawul",
                "Jere",
                "Kaga",
                "Kala-Balge",
                "Konduga",
                "Kukawa",
                "Kwaya Kusar",
                "Mafa",
                "Magumeri",
                "Maiduguri",
                "Marte",
                "Mobbar",
                "Monguno",
                "Ngala",
                "Nganzai",
                "Shani"
            ],
            "Cross River": [
                "Abi",
                "Akamkpa",
                "Akpabuyo",
                "Bakassi",
                "Bekwarra",
                "Biase",
                "Boki",
                "Calabar Municipal",
                "Calabar South",
                "Etung",
                "Ikom",
                "Obanliku",
                "Obubra",
                "Obudu",
                "Odukpani",
                "Ogoja",
                "Yakuur",
                "Yala"
            ],

            Delta: [
                "Aniocha North",
                "Aniocha South",
                "Bomadi",
                "Burutu",
                "Ethiope East",
                "Ethiope West",
                "Ika North East",
                "Ika South",
                "Isoko North",
                "Isoko South",
                "Ndokwa East",
                "Ndokwa West",
                "Okpe",
                "Oshimili North",
                "Oshimili South",
                "Patani",
                "Sapele",
                "Udu",
                "Ughelli North",
                "Ughelli South",
                "Ukwuani",
                "Uvwie",
                "Warri North",
                "Warri South",
                "Warri South West"
            ],

            Ebonyi: [
                "Abakaliki",
                "Afikpo North",
                "Afikpo South",
                "Ebonyi",
                "Ezza North",
                "Ezza South",
                "Ikwo",
                "Ishielu",
                "Ivo",
                "Izzi",
                "Ohaozara",
                "Ohaukwu",
                "Onicha"
            ],
            Edo: [
                "Akoko-Edo",
                "Egor",
                "Esan Central",
                "Esan North-East",
                "Esan South-East",
                "Esan West",
                "Etsako Central",
                "Etsako East",
                "Etsako West",
                "Igueben",
                "Ikpoba Okha",
                "Orhionmwon",
                "Oredo",
                "Ovia North-East",
                "Ovia South-West",
                "Owan East",
                "Owan West",
                "Uhunmwonde"
            ],

            Ekiti: [
                "Ado Ekiti",
                "Efon",
                "Ekiti East",
                "Ekiti South-West",
                "Ekiti West",
                "Emure",
                "Gbonyin",
                "Ido Osi",
                "Ijero",
                "Ikere",
                "Ikole",
                "Ilejemeje",
                "Irepodun-Ifelodun",
                "Ise-Orun",
                "Moba",
                "Oye"
            ],
            Rivers: [
                "Port Harcourt",
                "Obio-Akpor",
                "Okrika",
                "Ogu–Bolo",
                "Eleme",
                "Tai",
                "Gokana",
                "Khana",
                "Oyigbo",
                "Opobo–Nkoro",
                "Andoni",
                "Bonny",
                "Degema",
                "Asari-Toru",
                "Akuku-Toru",
                "Abua–Odual",
                "Ahoada West",
                "Ahoada East",
                "Ogba–Egbema–Ndoni",
                "Emohua",
                "Ikwerre",
                "Etche",
                "Omuma"
            ],
            Enugu: [
                "Aninri",
                "Awgu",
                "Enugu East",
                "Enugu North",
                "Enugu South",
                "Ezeagu",
                "Igbo Etiti",
                "Igbo Eze North",
                "Igbo Eze South",
                "Isi Uzo",
                "Nkanu East",
                "Nkanu West",
                "Nsukka",
                "Oji River",
                "Udenu",
                "Udi",
                "Uzo Uwani"
            ],
            FCT: [
                "Abaji",
                "Bwari",
                "Gwagwalada",
                "Kuje",
                "Kwali",
                "Municipal Area Council"
            ],
            Gombe: [
                "Akko",
                "Balanga",
                "Billiri",
                "Dukku",
                "Funakaye",
                "Gombe",
                "Kaltungo",
                "Kwami",
                "Nafada",
                "Shongom",
                "Yamaltu-Deba"
            ],
            Imo: [
                "Aboh Mbaise",
                "Ahiazu Mbaise",
                "Ehime Mbano",
                "Ezinihitte",
                "Ideato North",
                "Ideato South",
                "Ihitte-Uboma",
                "Ikeduru",
                "Isiala Mbano",
                "Isu",
                "Mbaitoli",
                "Ngor Okpala",
                "Njaba",
                "Nkwerre",
                "Nwangele",
                "Obowo",
                "Oguta",
                "Ohaji-Egbema",
                "Okigwe",
                "Orlu",
                "Orsu",
                "Oru East",
                "Oru West",
                "Owerri Municipal",
                "Owerri North",
                "Owerri West",
                "Unuimo"
            ],
            Jigawa: [
                "Auyo",
                "Babura",
                "Biriniwa",
                "Birnin Kudu",
                "Buji",
                "Dutse",
                "Gagarawa",
                "Garki",
                "Gumel",
                "Guri",
                "Gwaram",
                "Gwiwa",
                "Hadejia",
                "Jahun",
                "Kafin Hausa",
                "Kazaure",
                "Kiri Kasama",
                "Kiyawa",
                "Kaugama",
                "Maigatari",
                "Malam Madori",
                "Miga",
                "Ringim",
                "Roni",
                "Sule Tankarkar",
                "Taura",
                "Yankwashi"
            ],
            Kaduna: [
                "Birnin Gwari",
                "Chikun",
                "Giwa",
                "Igabi",
                "Ikara",
                "Jaba",
                "Jema a",
                "Kachia",
                "Kaduna North",
                "Kaduna South",
                "Kagarko",
                "Kajuru",
                "Kaura",
                "Kauru",
                "Kubau",
                "Kudan",
                "Lere",
                "Makarfi",
                "Sabon Gari",
                "Sanga",
                "Soba",
                "Zangon Kataf",
                "Zaria"
            ],
            Kano: [
                "Ajingi",
                "Albasu",
                "Bagwai",
                "Bebeji",
                "Bichi",
                "Bunkure",
                "Dala",
                "Dambatta",
                "Dawakin Kudu",
                "Dawakin Tofa",
                "Doguwa",
                "Fagge",
                "Gabasawa",
                "Garko",
                "Garun Mallam",
                "Gaya",
                "Gezawa",
                "Gwale",
                "Gwarzo",
                "Kabo",
                "Kano Municipal",
                "Karaye",
                "Kibiya",
                "Kiru",
                "Kumbotso",
                "Kunchi",
                "Kura",
                "Madobi",
                "Makoda",
                "Minjibir",
                "Nasarawa",
                "Rano",
                "Rimin Gado",
                "Rogo",
                "Shanono",
                "Sumaila",
                "Takai",
                "Tarauni",
                "Tofa",
                "Tsanyawa",
                "Tudun Wada",
                "Ungogo",
                "Warawa",
                "Wudil"
            ],
            Katsina: [
                "Bakori",
                "Batagarawa",
                "Batsari",
                "Baure",
                "Bindawa",
                "Charanchi",
                "Dandume",
                "Danja",
                "Dan Musa",
                "Daura",
                "Dutsi",
                "Dutsin Ma",
                "Faskari",
                "Funtua",
                "Ingawa",
                "Jibia",
                "Kafur",
                "Kaita",
                "Kankara",
                "Kankia",
                "Katsina",
                "Kurfi",
                "Kusada",
                "Mai Adua",
                "Malumfashi",
                "Mani",
                "Mashi",
                "Matazu",
                "Musawa",
                "Rimi",
                "Sabuwa",
                "Safana",
                "Sandamu",
                "Zango"
            ],
            Kebbi: [
                "Aleiro",
                "Arewa Dandi",
                "Argungu",
                "Augie",
                "Bagudo",
                "Birnin Kebbi",
                "Bunza",
                "Dandi",
                "Fakai",
                "Gwandu",
                "Jega",
                "Kalgo",
                "Koko Besse",
                "Maiyama",
                "Ngaski",
                "Sakaba",
                "Shanga",
                "Suru",
                "Wasagu Danko",
                "Yauri",
                "Zuru"
            ],
            Kogi: [
                "Adavi",
                "Ajaokuta",
                "Ankpa",
                "Bassa",
                "Dekina",
                "Ibaji",
                "Idah",
                "Igalamela Odolu",
                "Ijumu",
                "Kabba Bunu",
                "Kogi",
                "Lokoja",
                "Mopa Muro",
                "Ofu",
                "Ogori Magongo",
                "Okehi",
                "Okene",
                "Olamaboro",
                "Omala",
                "Yagba East",
                "Yagba West"
            ],
            Kwara: [
                "Asa",
                "Baruten",
                "Edu",
                "Ekiti",
                "Ifelodun",
                "Ilorin East",
                "Ilorin South",
                "Ilorin West",
                "Irepodun",
                "Isin",
                "Kaiama",
                "Moro",
                "Offa",
                "Oke Ero",
                "Oyun",
                "Pategi"
            ],
            Lagos: [
                "Agege",
                "Ajeromi-Ifelodun",
                "Alimosho",
                "Amuwo-Odofin",
                "Apapa",
                "Badagry",
                "Epe",
                "Eti Osa",
                "Ibeju-Lekki",
                "Ifako-Ijaiye",
                "Ikeja",
                "Ikorodu",
                "Kosofe",
                "Lagos Island",
                "Lagos Mainland",
                "Mushin",
                "Ojo",
                "Oshodi-Isolo",
                "Shomolu",
                "Surulere"
            ],
            Nasarawa: [
                "Akwanga",
                "Awe",
                "Doma",
                "Karu",
                "Keana",
                "Keffi",
                "Kokona",
                "Lafia",
                "Nasarawa",
                "Nasarawa Egon",
                "Obi",
                "Toto",
                "Wamba"
            ],
            Niger: [
                "Agaie",
                "Agwara",
                "Bida",
                "Borgu",
                "Bosso",
                "Chanchaga",
                "Edati",
                "Gbako",
                "Gurara",
                "Katcha",
                "Kontagora",
                "Lapai",
                "Lavun",
                "Magama",
                "Mariga",
                "Mashegu",
                "Mokwa",
                "Moya",
                "Paikoro",
                "Rafi",
                "Rijau",
                "Shiroro",
                "Suleja",
                "Tafa",
                "Wushishi"
            ],
            Ogun: [
                "Abeokuta North",
                "Abeokuta South",
                "Ado-Odo Ota",
                "Egbado North",
                "Egbado South",
                "Ewekoro",
                "Ifo",
                "Ijebu East",
                "Ijebu North",
                "Ijebu North East",
                "Ijebu Ode",
                "Ikenne",
                "Imeko Afon",
                "Ipokia",
                "Obafemi Owode",
                "Odeda",
                "Odogbolu",
                "Ogun Waterside",
                "Remo North",
                "Shagamu"
            ],
            Ondo: [
                "Akoko North-East",
                "Akoko North-West",
                "Akoko South-West",
                "Akoko South-East",
                "Akure North",
                "Akure South",
                "Ese Odo",
                "Idanre",
                "Ifedore",
                "Ilaje",
                "Ile Oluji-Okeigbo",
                "Irele",
                "Odigbo",
                "Okitipupa",
                "Ondo East",
                "Ondo West",
                "Ose",
                "Owo"
            ],
            Osun: [
                "Atakunmosa East",
                "Atakunmosa West",
                "Aiyedaade",
                "Aiyedire",
                "Boluwaduro",
                "Boripe",
                "Ede North",
                "Ede South",
                "Ife Central",
                "Ife East",
                "Ife North",
                "Ife South",
                "Egbedore",
                "Ejigbo",
                "Ifedayo",
                "Ifelodun",
                "Ila",
                "Ilesa East",
                "Ilesa West",
                "Irepodun",
                "Irewole",
                "Isokan",
                "Iwo",
                "Obokun",
                "Odo Otin",
                "Ola Oluwa",
                "Olorunda",
                "Oriade",
                "Orolu",
                "Osogbo"
            ],
            Oyo: [
                "Afijio",
                "Akinyele",
                "Atiba",
                "Atisbo",
                "Egbeda",
                "Ibadan North",
                "Ibadan North-East",
                "Ibadan North-West",
                "Ibadan South-East",
                "Ibadan South-West",
                "Ibarapa Central",
                "Ibarapa East",
                "Ibarapa North",
                "Ido",
                "Irepo",
                "Iseyin",
                "Itesiwaju",
                "Iwajowa",
                "Kajola",
                "Lagelu",
                "Ogbomosho North",
                "Ogbomosho South",
                "Ogo Oluwa",
                "Olorunsogo",
                "Oluyole",
                "Ona Ara",
                "Orelope",
                "Ori Ire",
                "Oyo",
                "Oyo East",
                "Saki East",
                "Saki West",
                "Surulere"
            ],
            Plateau: [
                "Bokkos",
                "Barkin Ladi",
                "Bassa",
                "Jos East",
                "Jos North",
                "Jos South",
                "Kanam",
                "Kanke",
                "Langtang South",
                "Langtang North",
                "Mangu",
                "Mikang",
                "Pankshin",
                "Qua an Pan",
                "Riyom",
                "Shendam",
                "Wase"
            ],
            Sokoto: [
                "Binji",
                "Bodinga",
                "Dange Shuni",
                "Gada",
                "Goronyo",
                "Gudu",
                "Gwadabawa",
                "Illela",
                "Isa",
                "Kebbe",
                "Kware",
                "Rabah",
                "Sabon Birni",
                "Shagari",
                "Silame",
                "Sokoto North",
                "Sokoto South",
                "Tambuwal",
                "Tangaza",
                "Tureta",
                "Wamako",
                "Wurno",
                "Yabo"
            ],
            Taraba: [
                "Ardo Kola",
                "Bali",
                "Donga",
                "Gashaka",
                "Gassol",
                "Ibi",
                "Jalingo",
                "Karim Lamido",
                "Kumi",
                "Lau",
                "Sardauna",
                "Takum",
                "Ussa",
                "Wukari",
                "Yorro",
                "Zing"
            ],
            Yobe: [
                "Bade",
                "Bursari",
                "Damaturu",
                "Fika",
                "Fune",
                "Geidam",
                "Gujba",
                "Gulani",
                "Jakusko",
                "Karasuwa",
                "Machina",
                "Nangere",
                "Nguru",
                "Potiskum",
                "Tarmuwa",
                "Yunusari",
                "Yusufari"
            ],
            Zamfara: [
                "Anka",
                "Bakura",
                "Birnin Magaji Kiyaw",
                "Bukkuyum",
                "Bungudu",
                "Gummi",
                "Gusau",
                "Kaura Namoda",
                "Maradun",
                "Maru",
                "Shinkafi",
                "Talata Mafara",
                "Chafe",
                "Zurmi"
            ]
        };

        let options = ["Select LGA..."]; // Default option

        if (state && lgaList[state]) {
            options = options.concat(lgaList[state]); // Append respective LGAs
        }

        frm.set_df_property("local_government_area", "options", options.join("\n"));
        frm.refresh_field("local_government_area"); // Refresh field to apply changes
    },

    pue_estimate_percent: function (frm) {
        let power = frm.doc.power_rating;
        let percent = frm.doc.pue_estimate_percent;

        // Calculate PUE Estimate kW
        let estimate_kw = (power * percent) / 100;
        // Set the calculated value
        frm.set_value("pue_estimate_kw", estimate_kw);
    },
    
    power_rating: function (frm) {
        if (frm.doc.power_rating && frm.doc.pue_estimate_percent) {
            let power = frm.doc.power_rating;
            let percent = frm.doc.pue_estimate_percent;

            // Calculate PUE Estimate kW
            let estimate_kw = (power * percent) / 100;
            // Set the calculated value
            frm.set_value("pue_estimate_kw", estimate_kw);
        }
    }
});

frappe.ui.form.on("Site Equipment Table", {
    allocation: function (frm, cdt, cdn) {


        calculate_max_rating(frm, cdt, cdn);
    },
    rating: function (frm, cdt, cdn) {
        console.log("Logggggg");
        calculate_quantity(frm, cdt, cdn)
    }
});


frappe.ui.form.on("Site", {
    pue_estimate_kw: function (frm) {
        frm.doc.max_rating.forEach(row => {
            calculate_max_rating(frm, row.doctype, row.name);
        });
        frm.refresh_field("max_rating"); // Refresh the child table to reflect updates
    }
});

function calculate_max_rating(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let equipment = frm.doc.equipment_name
    let total_per_allocation = 0
    equipment.forEach(row => {
        total_per_allocation = total_per_allocation + row.allocation

    })

    if (total_per_allocation < 100) {
        if (frm.doc.pue_estimate_kw && row.allocation && row.allocation != 0) {
            let max_rating = (frm.doc.pue_estimate_kw * row.allocation) / 100;

            frappe.model.set_value(cdt, cdn, "max_rating", max_rating);
        } else {
            frappe.model.set_value(cdt, cdn, "max_rating", 0); // Reset if allocation is 0 or missing
        }
    }
    else {
        console.log("failed")
        // Allocation can't exceed 100 percent.
        frappe.msgprint(__("Allocation can't exceed 100 percent."));
        
    }
}

function calculate_quantity(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (row.max_rating && row.rating != 0) {
        if (row.max_rating > row.rating) {
            let quantity = (row.max_rating) / (row.rating);

            frappe.model.set_value(cdt, cdn, "quantity", Math.floor(quantity));
        }
        else {
            frappe.model.set_value(cdt, cdn, "rating", 0);
            // Rating can't be more than Max Rating
            frappe.msgprint(__("Rating can't be more than Max Rating"));


        }
    } else {
        frappe.model.set_value(cdt, cdn, "quantity", 0); // Reset if allocation is 0 or missing
        // Max Rating can't be Zero
        frappe.msgprint(__("Max Rating can't be Zero"));
    }
}

frappe.ui.form.on('Site', {
    refresh: function(frm) {
        if (frm.is_new()) return;  // Don't fetch for unsaved docs

        // Clear existing data
        frm.clear_table('assigned_farmer');

        // Fetch Farmer Masters where site == current site
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Farmer Master',
                filters: {
                    site: frm.doc.name
                },
                fields: ['name', 'farmer_name', 'status'],
                limit_page_length: 100
            },
            callback: function(response) {
                const farmers = response.message || [];

                farmers.forEach(row => {
                    let child = frm.add_child('assigned_farmer');
                    child.farmer_name = row.name;
                    child.farmer = row.farmer_name;
                    child.status = row.status;
                });

                frm.refresh_field('assigned_farmer');
            }
        });
    }
});




//***************************************************************************************** */

// frappe.ui.form.on('Site', {
//     refresh: function(frm) {
//         if (frm.is_new()) return;

//         frm.clear_table('actual_crops');

//         // Step 1: Get Farmer Masters linked to this site
//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Farmer Master',
//                 filters: { site: frm.doc.name },
//                 fields: ['name'],
//                 limit_page_length: 100
//             },
//             callback: function(response) {
//                 let farmers = response.message || [];
//                 let allCropNames = new Set();
//                 let completed = 0;

//                 if (farmers.length === 0) {
//                     frm.refresh_field('actual_crops');
//                     return;
//                 }

//                 // Step 2: For each farmer, fetch full doc with farms child table
//                 farmers.forEach(farmer => {
//                     frappe.call({
//                         method: 'frappe.client.get',
//                         args: {
//                             doctype: 'Farmer Master',
//                             name: farmer.name
//                         },
//                         callback: function(docRes) {
//                             let farmerDoc = docRes.message;
//                             if (farmerDoc.farms) {
//                                 farmerDoc.farms.forEach(farm => {
//                                     if (farm.crops) {
//                                         allCropNames.add(farm.crops);
//                                     }
//                                 });
//                             }

//                             completed++;

//                             // Step 3: After all farmers fetched, add unique crops
//                             if (completed === farmers.length) {
//                                 allCropNames.forEach(crop => {
//                                     let row = frm.add_child('actual_crops');
//                                     row.crop_name = crop;
//                                 });
//                                 frm.refresh_field('actual_crops');
//                             }
//                         }
//                     });
//                 });
//             }
//         });
//     }
// });



frappe.ui.form.on('Site', {
    refresh: function(frm) {
        if (frm.is_new()) return;

        frm.clear_table('actual_crops');

        // Step 1: Get Farmer Masters linked to this site
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Farmer Master',
                filters: { site: frm.doc.name },
                fields: ['name'],
                limit_page_length: 100
            },
            callback: function(response) {
                let farmers = response.message || [];
                let allCropNames = new Set();
                let farmerNames = farmers.map(f => f.name);
                let completed = 0;

                if (farmerNames.length === 0) {
                    frm.refresh_field('actual_crops');
                    return;
                }

                // Step 2: Fetch all relevant Farm Master entries
                frappe.call({
                    method: 'frappe.client.get_list',
                    args: {
                        doctype: 'Farm Master',
                        filters: [['associated_farmer', 'in', farmerNames]],
                        fields: ['name', 'associated_farmer'],
                        limit_page_length: 100
                    },
                    callback: function(farmResponse) {
                        let farms = farmResponse.message || [];
                        let farmCompleted = 0;
                        let cropQuantityMap = {};

                        if (farms.length === 0) {
                            frm.refresh_field('actual_crops');
                            return;
                        }

                        farms.forEach(farm => {
                            // Get full Farm Master doc with actual_crops child table
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: 'Farm Master',
                                    name: farm.name
                                },
                                callback: function(farmDocRes) {
                                    let farmDoc = farmDocRes.message;
                                    if (farmDoc.actual_crops && Array.isArray(farmDoc.actual_crops)) {
                                        farmDoc.actual_crops.forEach(cropRow => {
                                            let cropName = cropRow.crop_name;
                                            let qty = parseFloat(cropRow.quantity) || 0;

                                            if (!cropQuantityMap[cropName]) {
                                                cropQuantityMap[cropName] = 0;
                                            }
                                            cropQuantityMap[cropName] += qty;

                                            allCropNames.add(cropName);
                                        });
                                    }

                                    farmCompleted++;

                                    // Step 3: After all farm docs processed, add unique crops and quantity
                                    if (farmCompleted === farms.length) {
                                        allCropNames.forEach(crop => {
                                            let row = frm.add_child('actual_crops');
                                            row.crop_name = crop;
                                            row.quantity = cropQuantityMap[crop] || 0;
                                        });
                                        frm.refresh_field('actual_crops');
                                    }
                                }
                            });
                        });
                    }
                });
            }
        });
    }
});
