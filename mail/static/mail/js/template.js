var invi_ko = {
    "values": [
        "target",
        "name",
        "age"
    ],
    "template": [
        "안녕하십니까. {target}님, KAIST 국제 대학생 컨퍼런스 ICISTS(아이시스츠) 조직위원회 {name}입니다.",
        "",
        "이번 ICISTS에 연사로 초청하기 위해 연락을 드립니다.",
        "",
        "만약 ICISTS에 강연을 하고 싶으시다면 답신바랍니다.",
        "읽어주셔셔 감사합니다",
        "{name}{name}{age}"
    ]
}



function load_template() {
    var invi = invi_ko;
    
    document.getElementById("id_values").innerText = invi.template;
}