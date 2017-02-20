using Microsoft.VisualStudio.TestPlatform.ObjectModel.Adapter;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestPlatform.ObjectModel;

namespace VisualStudioTestAdapter
{
	public class Executor : ITestExecutor
	{
		public const string ExecutorUriString = "executor://PunitTestExecutor/v1";
		public static readonly Uri ExecutorUri = new Uri( ExecutorUriString );

		public void Cancel()
		{
			throw new NotImplementedException();
		}

		public void RunTests( IEnumerable<string> sources, IRunContext runContext, IFrameworkHandle frameworkHandle )
		{
			throw new NotImplementedException();
		}

		public void RunTests( IEnumerable<TestCase> tests, IRunContext runContext, IFrameworkHandle frameworkHandle )
		{
			throw new NotImplementedException();
		}
	}
}
