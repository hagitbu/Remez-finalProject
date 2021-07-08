// window.onload = function () {
//
//     var chart = new CanvasJS.Chart("chartContainer", {
//         animationEnabled: true,
//         title:{
//             text: "מספר התרגילים שבוצעו לפי סוג פונקציה"
//         },
//         axisY: {
//             title: "מספר התרגילים שבוצעו",
//             titleFontColor: "#000000",
//             lineColor: "#000000",
//             labelFontColor: "#000000",
//             tickColor: "#000000"
//         },
//
//         toolTip: {
//             shared: true
//         },
//         legend: {
//             cursor:"pointer",
//             itemclick: toggleDataSeries
//         },
//         data: [{
//             type: "column",
//             name: "ללא שורש או מנה",
//             legendText: "ללא שורש או מנה",
//             showInLegend: true,
//             dataPoints:[
//                 { label: "פולינום", y: 1 },
//                 { label: "מעריכית", y: 6 },
//                 { label: "לוגריתמית", y: 8 },
//                 { label: "טריגונומטרית", y: 3 },
//
//             ]
//         },
//
//             {
//                 type: "column",
//                 name: "מנה",
//                 legendText: "מנה",
//                 showInLegend: true,
//                 dataPoints:[
//                     { label: "פולינום", y: 5 },
//                     { label: "מעריכית", y: 6 },
//                     { label: "לוגריתמית", y: 3 },
//                     { label: "טריגונומטרית", y: 2 },
//
//                 ]
//             },
//
//             {
//                 type: "column",
//                 name: "שורש",
//                 legendText: "שורש",
//                 axisYType: "secondary",
//                 showInLegend: true,
//                 dataPoints:[
//                     { label: "פולינום", y: 8 },
//                     { label: "מעריכית", y: 5 },
//                     { label: "לוגריתמית", y: 7 },
//                     { label: "טריגונומטרית", y: 2 },
//
//                 ]
//             }]
//     });
//     chart.render();
//
//     function toggleDataSeries(e) {
//         if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
//             e.dataSeries.visible = false;
//         }
//         else {
//             e.dataSeries.visible = true;
//         }
//         chart.render();
//     }
//
// }