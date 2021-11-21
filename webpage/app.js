const FilePath = "./testData.json"; //TODO: change to real path

async function getData() {
    let courses = await fetch(FilePath);
    let coursesJson = await courses.json();
    return coursesJson;
}