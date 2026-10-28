using CoreContracts;
namespace CoreContracts { public enum ModuleRole { Support } }
namespace PortableConsumers.ModuleRole
{
    internal sealed class Catalog { internal object Value => ModuleRole.Support; }
}
