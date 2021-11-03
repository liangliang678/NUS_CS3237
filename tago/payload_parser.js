const ignore_vars = [];

function toTagoFormat(object_item)
{
  object_item = object_item['d'];
  const result = [];
  for (const key in object_item) {
    if (ignore_vars.includes(key)) continue;

    result.push({
      variable: key,
      value: object_item[key],
      time: new Date().getTime()
    });
  }

  return result;
}

payload = toTagoFormat(payload[0]);
