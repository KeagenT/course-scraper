const FilePath = "./testData.json"; //TODO: change to real path

var nameToIndex = {};

async function getData() {
    let courses = await fetch(FilePath);
    let coursesJson = await courses.json();
    buildNameToIndex(coursesJson);
    return coursesJson;
}

//Builds the name to index dictionary
function buildNameToIndex(data) {
    let n = 0;
    for (let course of data) {
        nameToIndex[course["ID"]] = n;
        n++;
    }
}

//Function for recursively building a tree data structure for visualization 
function buildTree(parent, node, data) {
    let index = nameToIndex[node["name"]];
    let children = data[index]["Prerequisites"];

    for (let name of children) {
        node["children"].push({
            "name": name,
            "parent": node["name"],
            "children": []
        })
    }

    for (let child of node["children"]) {
        buildTree(node, child, data);
    }
}

function displayCourse(course) {
    var courseID = document.getElementById("courseID");
    var courseName = document.getElementById("courseName");
    var courseDesc = document.getElementById("courseDesc");
    courseID.innerHTML = "ID: " + course["ID"];
    courseName.innerHTML = "NAME: " + course["Name"];
    courseDesc.innerHTML = "DESCRIPTION: " + course["Description"];
}

function getSearch() {
    var field = document.getElementById("field");
    let value = field.value;
    field.value = "";
    return value;
}

function getCourse(search, data) {
    return data[nameToIndex[search]];
}