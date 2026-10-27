using Cehpalon.Engine.Composition;
using System.Text.Json;
var catalog = new[] { new ModuleDescriptor("core", ModuleRole.Support) };
var valid = "{\"Cehpalon\":{\"SchemaVersion\":1,\"Architecture\":\"Modular\",\"Topology\":\"SingleProcess\",\"Pattern\":\"RequestReply\",\"Modules\":{\"core\":{\"Enabled\":true}}}}";
foreach (var test in new[] { ("invalid-profile-surrogate", valid.Replace("Modular", "\\uD800")), ("invalid-module-name-surrogate",valid.Replace("core", "\\uD800")), ("invalid-property-name-surrogate", valid.Replace("Architecture", "\\uD800")) })
{
    try
    {
        var result = CompositionCompiler.Compile(test.Item2, catalog);
        Console.WriteLine(JsonSerializer.Serialize(new { name=test.Item1, result=result.IsSuccess, diagnostics=result.Diagnostics.Select(x=>x.Code) }));
    }
    catch (Exception error)
    {
        Console.WriteLine(JsonSerializer.Serialize(new { name=test.Item1, exception=error.GetType().Name, message=error.Message }));
    }
}
