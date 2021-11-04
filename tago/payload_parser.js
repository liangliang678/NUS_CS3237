const ignore_vars = [];

function toTagoFormat(object_item)
{
  // if your gateway is iOS, comment it
  object_item = object_item['d'];

  time = new Date().getTime();
  const result = [];
  for (const key in object_item) {
    if (ignore_vars.includes(key)) continue;

    result.push({
      variable: key,
      value: object_item[key],
      serie: object_item.serie || time,
      time: time
    });
  }

  return result;
}

payload = toTagoFormat(payload[0]);
