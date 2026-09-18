/**
 * =========================================================================
 * MVP 부모유형 진단 - 구글 스프레드시트 자동 연동 Google Apps Script (GAS)
 * =========================================================================
 * 
 * [수정된 내용: 일시 바로 옆 B열에 '이름' 추가]
 * - 기존 시트에 '이름' 열이 없으면 자동으로 B열에 '이름'을 삽입합니다.
 * 
 * [배포 업데이트 방법]
 * 1. Apps Script(Code.gs) 화면에서 아래 코드로 전체 교체합니다.
 * 2. 상단 [저장] (Ctrl + S)을 누릅니다.
 * 3. 우측 상단 파란색 [배포] 버튼 클릭 > [배포 관리] 선택
 * 4. 활성 배포 옆의 [연필 아이콘(수정)] 클릭
 * 5. 버전: [새 버전] 선택 후 우측 하단 [배포] 클릭!
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  // 동시 접속 시 10초간 대기
  lock.tryLock(10000);

  try {
    var doc = SpreadsheetApp.getActiveSpreadsheet();
    // 'mvp' 또는 'mvp01' 이름의 시트를 찾고, 없으면 첫 번째 활성 시트 사용
    var sheet = doc.getSheetByName("mvp") || doc.getSheetByName("mvp01") || doc.getSheets()[0];

    // 1. 시트가 비어있으면 헤더 행 전체 자동 생성
    if (sheet.getLastRow() === 0) {
      var headers = [
        "일시", "이름", "주 유형", "부 유형",
        "공감형(A)", "훈육형(B)", "자율형(C)", "균형형(D)",
        "접속 기기", "상세 응답(JSON)"
      ];
      sheet.appendRow(headers);

      // 헤더 스타일 적용 (볼드, 오렌지 배경, 중앙 정렬)
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setFontWeight("bold");
      headerRange.setBackground("#ffe8cc");
      headerRange.setHorizontalAlignment("center");
      sheet.setFrozenRows(1);
    } else {
      // 2. 이미 시트가 있는 경우: B열이 '이름'이 아니면 자동으로 B열에 '이름' 컬럼 삽입
      var firstRowValues = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 2)).getValues()[0];
      if (firstRowValues[1] !== "이름") {
        sheet.insertColumnBefore(2);
        sheet.getRange(1, 2)
          .setValue("이름")
          .setFontWeight("bold")
          .setBackground("#ffe8cc")
          .setHorizontalAlignment("center");
      }
    }

    var data = {};
    if (e && e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (err) {
        data = e.parameter || {};
      }
    } else if (e && e.parameter) {
      data = e.parameter;
    }

    var now = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");

    var rowData = [
      data.timestamp || now,
      data.name || "익명",
      data.primaryType || "",
      data.secondaryType || "",
      data.scoreA !== undefined ? data.scoreA : 0,
      data.scoreB !== undefined ? data.scoreB : 0,
      data.scoreC !== undefined ? data.scoreC : 0,
      data.scoreD !== undefined ? data.scoreD : 0,
      data.device || "",
      typeof data.responses === "object" ? JSON.stringify(data.responses) : (data.responses || "")
    ];

    sheet.appendRow(rowData);

    // 마지막 추가된 행 가운데 정렬
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1, 1, rowData.length).setHorizontalAlignment("center");

    return ContentService.createTextOutput(JSON.stringify({ result: "success", row: lastRow }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ result: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// GET 요청 테스트용
function doGet(e) {
  return ContentService.createTextOutput("MVP 부모유형 진단 Google Apps Script 웹 앱이 정상 동작 중입니다.")
    .setMimeType(ContentService.MimeType.TEXT);
}
