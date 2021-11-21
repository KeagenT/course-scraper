const FilePath = "./testData.json";

async function getData() {
    let courses = await fetch(FilePath);
    let coursesJson = await courses.json();
    return coursesJson;
}